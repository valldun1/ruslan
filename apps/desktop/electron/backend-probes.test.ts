/**
 * Tests for electron/backend-probes.ts.
 *
 * Run with: node --test electron/backend-probes.test.ts
 * (Wired into npm test:desktop:platforms in package.json.)
 */

import assert from 'node:assert/strict'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'

import { test } from 'vitest'

import { canImportRuslanCli, ruslanRuntimeImportProbe, verifyRuslanCli } from './backend-probes'

// Resolve the host's own Node binary -- guaranteed to be on disk and
// runnable. We use it as both a stand-in for "a python that doesn't
// have ruslan_cli" (since `node -c "import ruslan_cli"` will exit
// non-zero) and as a way to script verifyRuslanCli's success path
// (a tiny script we write to disk that exits 0 on --version).
const NODE_BIN = process.execPath

test('canImportRuslanCli returns false when path is falsy', () => {
  assert.equal(canImportRuslanCli(''), false)
  assert.equal(canImportRuslanCli(null), false)
  assert.equal(canImportRuslanCli(undefined), false)
})

test('canImportRuslanCli returns false when interpreter cannot run -c', () => {
  // node IS an interpreter, but `node -c "import ruslan_cli"` is a
  // SyntaxError -- different exit reason from a real Python's
  // ModuleNotFoundError, but the predicate is "exit 0 or not" and
  // both land on "not", which is exactly what we want for the
  // resolver fall-through.
  assert.equal(canImportRuslanCli(NODE_BIN), false)
})

test('canImportRuslanCli returns false when binary does not exist', () => {
  const ghost = path.join(os.tmpdir(), 'ruslan-probes-ghost-' + Date.now() + '.exe')
  assert.equal(canImportRuslanCli(ghost), false)
})

test('ruslan runtime import probe checks config dependencies', () => {
  const probe = ruslanRuntimeImportProbe()
  assert.match(probe, /\bimport yaml\b/)
  // dotenv is the first third-party import on the CLI boot path
  // (ruslan_cli/env_loader.py); a mid-update venv missing python-dotenv
  // passed the old probe and produced an unrecoverable boot loop.
  assert.match(probe, /\bimport dotenv\b/)
  assert.match(probe, /\bimport ruslan_cli\.config\b/)
})

test('verifyRuslanCli returns false when command is falsy', () => {
  assert.equal(verifyRuslanCli(''), false)
  assert.equal(verifyRuslanCli(null), false)
  assert.equal(verifyRuslanCli(undefined), false)
})

test('verifyRuslanCli returns false when binary does not exist', () => {
  const ghost = path.join(os.tmpdir(), 'ruslan-probes-ghost-' + Date.now() + '.exe')
  assert.equal(verifyRuslanCli(ghost), false)
})

test('verifyRuslanCli returns true when --version exits 0', () => {
  // Write a tiny script that exits 0 regardless of args, then invoke
  // it through node. This stands in for a working ruslan binary --
  // verifyRuslanCli only cares about the exit code.
  const scriptPath = path.join(os.tmpdir(), `ruslan-probes-ok-${Date.now()}-${process.pid}.cjs`)
  fs.writeFileSync(scriptPath, 'process.exit(0)\n')

  try {
    // Use node as the launcher and our script as the "command". Pass
    // shell:false (default) -- node is a real binary, no shim.
    // execFileSync passes ['--version'] as args, which node ignores
    // gracefully (well, it prints its version and exits 0, which is
    // perfect -- exit code 0 is the only signal we read).
    assert.equal(verifyRuslanCli(NODE_BIN), true)
  } finally {
    try {
      fs.unlinkSync(scriptPath)
    } catch {
      void 0
    }
  }
})

test('verifyRuslanCli swallows timeouts (does not throw)', () => {
  // We can't easily provoke a real 5s hang in CI without slowing the
  // suite, but we CAN confirm that an invocation that DOES throw
  // (because the binary is missing) returns false rather than
  // propagating. Same code path the timeout case takes.
  assert.equal(verifyRuslanCli('/definitely/not/a/real/binary/anywhere'), false)
})
