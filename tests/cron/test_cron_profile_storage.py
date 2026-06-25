"""Regression tests for #32091 — profile-scoped cron jobs orphaned.

Cron storage (CRON_DIR/JOBS_FILE) must anchor at the *default root* Ruslan
home, not the active profile's home. Otherwise a job created from a
profile-scoped agent session writes to ~/.ruslan/profiles/<p>/cron/jobs.json,
while the profile-less gateway reads only ~/.ruslan/cron/jobs.json — the job
is silently orphaned (looks healthy in `list`, never fires).
"""
import importlib
import os
from pathlib import Path


def test_cron_storage_anchors_at_root_under_profile(tmp_path, monkeypatch):
    """Under a profile RUSLAN_HOME (<root>/profiles/<name>), the cron store
    resolves to <root>/cron, NOT <root>/profiles/<name>/cron."""
    root = tmp_path / "ruslan_home"
    profile_home = root / "profiles" / "myprofile"
    profile_home.mkdir(parents=True)

    # Pretend the platform default root IS our tmp root, and the active
    # RUSLAN_HOME is a profile under it (the #32091 scenario).
    import ruslan_constants
    monkeypatch.setattr(ruslan_constants, "_get_platform_default_ruslan_home",
                        lambda: root)
    monkeypatch.setenv("RUSLAN_HOME", str(profile_home))

    # get_default_ruslan_root must return the ROOT, not the profile dir.
    assert ruslan_constants.get_default_ruslan_root().resolve() == root.resolve()
    # ...while get_ruslan_home (used elsewhere) follows the profile override.
    assert ruslan_constants.get_ruslan_home().resolve() == profile_home.resolve()

    # cron/jobs.py computes RUSLAN_DIR from get_default_ruslan_root at import,
    # so a fresh import under this env anchors the store at <root>/cron.
    import cron.jobs as jobs
    importlib.reload(jobs)
    try:
        assert jobs.RUSLAN_DIR.resolve() == root.resolve()
        assert jobs.JOBS_FILE.resolve() == (root / "cron" / "jobs.json").resolve()
        # The orphan path (<profile>/cron/jobs.json) must NOT be the store.
        assert jobs.JOBS_FILE.resolve() != (profile_home / "cron" / "jobs.json").resolve()
    finally:
        # Restore module state for other tests (reload under the real env).
        monkeypatch.undo()
        importlib.reload(jobs)


def test_cron_storage_unaffected_when_no_profile(tmp_path, monkeypatch):
    """With no profile (RUSLAN_HOME == root), behavior is unchanged: store at
    <root>/cron."""
    root = tmp_path / "ruslan_home"
    root.mkdir(parents=True)
    import ruslan_constants
    monkeypatch.setattr(ruslan_constants, "_get_platform_default_ruslan_home",
                        lambda: root)
    monkeypatch.setenv("RUSLAN_HOME", str(root))

    import cron.jobs as jobs
    importlib.reload(jobs)
    try:
        assert jobs.JOBS_FILE.resolve() == (root / "cron" / "jobs.json").resolve()
    finally:
        monkeypatch.undo()
        importlib.reload(jobs)


def test_tick_lock_anchors_at_root_under_profile(tmp_path, monkeypatch):
    """The cron tick lock must live at <root>/cron/.tick.lock, NOT the profile
    dir — otherwise tickers under different profiles grab different locks and
    double-fire the (now root-anchored) jobs store (#32091)."""
    import importlib
    root = tmp_path / "ruslan_home"
    profile_home = root / "profiles" / "p"
    profile_home.mkdir(parents=True)
    import ruslan_constants
    monkeypatch.setattr(ruslan_constants, "_get_platform_default_ruslan_home", lambda: root)
    monkeypatch.setenv("RUSLAN_HOME", str(profile_home))
    import cron.scheduler as sched
    importlib.reload(sched)
    try:
        # _ruslan_home override is None -> uses get_default_ruslan_root()
        sched._ruslan_home = None
        lock_dir, lock_file = sched._get_lock_paths()
        assert lock_dir.resolve() == (root / "cron").resolve()
        assert lock_file.resolve() == (root / "cron" / ".tick.lock").resolve()
        assert lock_dir.resolve() != (profile_home / "cron").resolve()
    finally:
        monkeypatch.undo()
        importlib.reload(sched)


def test_get_default_ruslan_root_docker_layouts(tmp_path, monkeypatch):
    """get_default_ruslan_root resolves the root for Docker/custom RUSLAN_HOME
    (outside ~/.ruslan), so cron storage works in containers."""
    import ruslan_constants
    native = tmp_path / "native_home"
    monkeypatch.setattr(ruslan_constants, "_get_platform_default_ruslan_home", lambda: native)

    # Docker custom root (outside native): RUSLAN_HOME itself IS the root.
    monkeypatch.setenv("RUSLAN_HOME", "/opt/data")
    assert ruslan_constants.get_default_ruslan_root() == Path("/opt/data")

    # Docker profile layout: <custom>/profiles/<name> -> <custom>.
    monkeypatch.setenv("RUSLAN_HOME", "/opt/data/profiles/coder")
    assert ruslan_constants.get_default_ruslan_root() == Path("/opt/data")
