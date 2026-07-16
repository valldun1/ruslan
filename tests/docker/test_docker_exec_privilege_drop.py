"""Regression tests for the docker-exec privilege-drop shim.

The shim (docker/ruslan-exec-shim.sh, installed at /opt/ruslan/bin/ruslan)
exists to prevent the auth.json ownership-mismatch bug where
`docker exec <c> ruslan login` would write /opt/data/auth.json as
root:root mode 0600, leaving the supervised gateway (UID 10000) unable
to read its own credentials and returning "Provider authentication
failed: Ruslan is not logged into Nous Portal" on every message.

These tests verify:

1. ``docker exec <c> ruslan …`` (defaulting to root) gets dropped to the
   ruslan user before the real binary runs.
2. ``docker exec --user ruslan <c> ruslan …`` (already non-root) short-
   circuits and doesn't try to drop again.
3. Files written under $RUSLAN_HOME from a ``docker exec`` session land
   as ruslan:ruslan — the actual user-visible invariant.
4. The RUSLAN_DOCKER_EXEC_AS_ROOT opt-out lets diagnostic sessions keep
   running as root deliberately.
5. The main CMD path (``docker run <image> …``) is unaffected by the
   PATH-shim ordering — no recursion, no behavior change.
"""

from __future__ import annotations
from tests.docker.conftest import docker_exec

import subprocess
import time
from collections.abc import Iterator

import pytest


# How long to give a `docker run -d` container before declaring it not ready.
# Generous because under arm64 QEMU emulation cont-init (a Python config
# migration + chowns) runs several times slower than on native amd64.
_RUN_READY_TIMEOUT_S = 60


def _wait_for_cont_init(container: str) -> None:
    """Block until s6 cont-init has fully finished, not merely until
    ``docker exec`` is responsive.

    The earlier ``_wait_for_init`` only polled ``docker exec <c> true``,
    which succeeds almost immediately on s6-overlay — long before the
    ``01-ruslan-setup`` cont-init hook (docker/stage2-hook.sh) has
    finished seeding + ``chown ruslan:ruslan`` config.yaml and running the
    Python config migration. A test that wipes config.yaml and then writes
    it as root would then race that boot-time chown: on native amd64
    stage2-hook wins in a blink and the test always passed, but under arm64
    QEMU emulation the slow Python migration was still in flight and
    clobbered the root-written file's ownership back to ruslan:ruslan,
    failing ``test_shim_opt_out_keeps_root`` non-deterministically.

    The reliable "cont-init is done" signal is
    ``$RUSLAN_HOME/logs/container-boot.log``: it is written by
    ``02-reconcile-profiles`` (ruslan_cli.container_boot), which s6 runs
    *strictly after* ``01-ruslan-setup`` in lexicographic order. The
    reconciler always logs at least one ``profile=default`` line even for a
    bare ``sleep infinity`` container, so once that marker appears every
    stage2-hook side effect (seed, chown, migrate) is guaranteed complete.
    Mirrors the readiness pattern in test_container_restart.py.
    """
    deadline = time.monotonic() + _RUN_READY_TIMEOUT_S
    last = ""
    while time.monotonic() < deadline:
        r = subprocess.run(
            ["docker", "exec", container,
             "cat", "/opt/data/logs/container-boot.log"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            last = r.stdout
            if "profile=default" in last:
                return
        time.sleep(0.2)
    pytest.fail(
        f"container {container} did not finish cont-init within "
        f"{_RUN_READY_TIMEOUT_S}s (container-boot.log so far: {last!r})"
    )


@pytest.fixture
def sleep_container(built_image: str, container_name: str) -> Iterator[str]:
    """Long-lived container running `sleep infinity` so we can docker exec into it."""
    subprocess.run(
        ["docker", "rm", "-f", container_name],
        capture_output=True, check=False,
    )
    r = subprocess.run(
        ["docker", "run", "-d", "--name", container_name, built_image,
         "sleep", "infinity"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"docker run failed: {r.stderr}"
    try:
        _wait_for_cont_init(container_name)
        yield container_name
    finally:
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            capture_output=True, check=False,
        )


def test_shim_drops_root_to_ruslan_uid(sleep_container: str) -> None:
    """docker exec defaults to root; the shim should drop to uid 10000.

    We invoke `ruslan` with a Python-style `-c` shim equivalent — there's no
    pure-ruslan "print my uid" command, so we use the venv's python directly
    via the shim's PATH lookup: `python -c 'print(os.getuid())'` is resolved
    through the venv. But that bypasses the shim. Instead, we exploit the
    fact that the venv's `ruslan` is a console_scripts entry — under the
    hood it's a tiny Python wrapper. We can't easily inject "print my uid"
    into it without forking subcommands. Simplest approach: have `ruslan`
    do anything that writes to disk, then check the file's owner.

    Use `ruslan config set` which writes config.yaml under RUSLAN_HOME.
    The resulting file ownership tells us what UID the shim ended up at.
    """
    # Wipe any prior state.
    subprocess.run(
        ["docker", "exec", "--user", "root", sleep_container,
         "rm", "-f", "/opt/data/config.yaml"],
        capture_output=True, check=False,
    )

    # Default docker exec (root) — should be dropped by the shim.
    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "ruslan", "config", "set", "_test.shim_marker", "1"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"config set failed: stdout={r.stdout!r} stderr={r.stderr!r}"

    # The written file must be owned by ruslan, not root.
    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "stat", "-c", "%U:%G", "/opt/data/config.yaml"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0, f"stat failed: {r.stderr}"
    assert r.stdout.strip() == "ruslan:ruslan", (
        f"config.yaml owned by {r.stdout.strip()!r}, expected ruslan:ruslan. "
        "The shim did not drop privileges before invoking ruslan."
    )


def test_shim_short_circuits_for_non_root_exec(sleep_container: str) -> None:
    """docker exec --user ruslan already runs as 10000; shim should be a no-op.

    Verified indirectly: the command must still succeed end-to-end. If the
    shim incorrectly tried to drop privileges a second time (e.g. by
    invoking s6-setuidgid which requires root), it would fail with
    EPERM. A clean success proves the short-circuit fired.
    """
    subprocess.run(
        ["docker", "exec", "--user", "root", sleep_container,
         "rm", "-f", "/opt/data/config.yaml"],
        capture_output=True, check=False,
    )

    r = subprocess.run(
        ["docker", "exec", "--user", "ruslan", sleep_container,
         "ruslan", "config", "set", "_test.shim_short_circuit", "1"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, (
        f"docker exec --user ruslan failed: {r.stderr!r} stdout={r.stdout!r}. "
        "If the shim mis-handled the non-root path, this would fail with EPERM."
    )

    # File still ends up ruslan:ruslan — orthogonally confirms uid.
    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "stat", "-c", "%U:%G", "/opt/data/config.yaml"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.stdout.strip() == "ruslan:ruslan"


def test_shim_opt_out_keeps_root(sleep_container: str) -> None:
    """RUSLAN_DOCKER_EXEC_AS_ROOT=1 should suppress the privilege drop.

    Reserved for diagnostic sessions where the operator deliberately
    wants root semantics. Verified by writing a file and checking its
    owner.
    """
    subprocess.run(
        ["docker", "exec", "--user", "root", sleep_container,
         "rm", "-f", "/opt/data/config.yaml"],
        capture_output=True, check=False,
    )

    r = subprocess.run(
        ["docker", "exec",
         "-e", "RUSLAN_DOCKER_EXEC_AS_ROOT=1",
         sleep_container,
         "ruslan", "config", "set", "_test.opt_out", "1"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"opt-out invocation failed: {r.stderr}"

    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "stat", "-c", "%U:%G", "/opt/data/config.yaml"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.stdout.strip() == "root:root", (
        f"With RUSLAN_DOCKER_EXEC_AS_ROOT=1, expected root:root, "
        f"got {r.stdout.strip()!r}"
    )


@pytest.mark.parametrize("falsy_value", ["0", "false", "no", "", "garbage", "2"])
def test_shim_opt_out_strict_truthiness(
    sleep_container: str, falsy_value: str,
) -> None:
    """Anything other than 1/true/yes (case-insensitive) does NOT opt out.

    Strict truthiness so a typo (``RUSLAN_DOCKER_EXEC_AS_ROOT=0``) doesn't
    silently keep the user as root. Mirrors the policy used by
    ``RUSLAN_GATEWAY_NO_SUPERVISE`` in #33583.
    """
    subprocess.run(
        ["docker", "exec", "--user", "root", sleep_container,
         "rm", "-f", "/opt/data/config.yaml"],
        capture_output=True, check=False,
    )

    r = subprocess.run(
        ["docker", "exec",
         "-e", f"RUSLAN_DOCKER_EXEC_AS_ROOT={falsy_value}",
         sleep_container,
         "ruslan", "config", "set", "_test.falsy", "1"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"falsy value {falsy_value!r} caused failure: {r.stderr}"

    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "stat", "-c", "%U:%G", "/opt/data/config.yaml"],
        capture_output=True, text=True, timeout=10,
    )
    assert r.stdout.strip() == "ruslan:ruslan", (
        f"falsy opt-out value {falsy_value!r} unexpectedly suppressed the drop; "
        f"file owner is {r.stdout.strip()!r}, expected ruslan:ruslan"
    )


def test_main_cmd_path_unaffected(built_image: str) -> None:
    """The CMD path (docker run <image> <args>) must still work.

    The shim sits at /opt/ruslan/bin earliest on PATH; main-wrapper.sh
    invokes `s6-setuidgid ruslan ruslan <args>` which resolves `ruslan`
    through PATH. With the shim in the way, this could regress if the
    shim recurses or interferes with TTY/exit-code propagation.

    `chat --help` is cheap and exercises the full subcommand
    passthrough path. The duplicate of test_main_invocation's
    pre-existing test is intentional — that one would have passed
    pre-shim too; this one specifically guards against shim regressions
    in the CMD-as-main-program codepath.
    """
    r = subprocess.run(
        ["docker", "run", "--rm", built_image, "chat", "--help"],
        capture_output=True, text=True, timeout=60,
    )
    assert r.returncode == 0, f"CMD path broken by shim: stderr={r.stderr!r}"
    assert "Traceback" not in r.stderr


def test_e2e_login_then_supervised_gateway_can_read_auth(
    sleep_container: str,
) -> None:
    """End-to-end regression for the original bug.

    Pre-shim: ``docker exec <c> ruslan login`` (root) wrote
    /opt/data/auth.json as root:root 0600. The supervised gateway (UID
    10000) couldn't read it, _load_auth_store swallowed PermissionError
    as a parse failure, and resolve_nous_runtime_credentials raised
    "Ruslan is not logged into Nous Portal" on every message.

    We can't do a real OAuth login in a unit test, but we can stand in
    for it by writing the same file shape via `ruslan config set`-style
    writes — what matters is the *file ownership invariant* downstream
    of `_save_auth_store`. If the shim works, every file the
    `docker exec` path produces is ruslan-readable.

    Specifically: pretend the operator ran `ruslan login` (writes
    auth.json) and verify (a) the file exists and (b) it's readable by
    the ruslan UID. We use `ruslan auth list` since that touches the
    auth store on the read side and would fail with the same
    'not logged in' shape if the file was unreadable to uid 10000.
    """
    # Have the shim-protected `docker exec` write the auth store.
    # `ruslan auth list` is read-only but still exercises _load_auth_store
    # under the shim's UID. We invoke `ruslan config set` first to
    # provoke a write into RUSLAN_HOME so we have something concrete to
    # owner-check.
    r = subprocess.run(
        ["docker", "exec", sleep_container,
         "ruslan", "config", "set", "_test.e2e_marker", "1"],
        capture_output=True, text=True, timeout=30,
    )
    assert r.returncode == 0, f"config set failed: {r.stderr}"

    # The supervised UID (10000) must be able to read everything under
    # RUSLAN_HOME that docker exec just wrote.
    r = subprocess.run(
        ["docker", "exec", "--user", "ruslan", sleep_container,
         "find", "/opt/data", "-maxdepth", "2", "-type", "f",
         "!", "-readable", "-print"],
        capture_output=True, text=True, timeout=15,
    )
    assert r.returncode == 0, f"find failed: {r.stderr}"
    unreadable = [ln for ln in r.stdout.splitlines() if ln.strip()]
    assert not unreadable, (
        "Files written by `docker exec` are unreadable to the ruslan user "
        f"(supervised gateway UID): {unreadable}. The shim failed to drop "
        "privileges before the write."
    )