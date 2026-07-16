import assert from 'node:assert/strict'
import path from 'node:path'

import { test } from 'vitest'

import {
  appendUniquePathEntries,
  buildDesktopBackendEnv,
  buildDesktopBackendPath,
  normalizeRuslanHomeRoot,
  pathEnvKey,
  POSIX_SANE_PATH_ENTRIES
} from './backend-env'

test('desktop backend PATH adds Ruslan-managed bins and missing POSIX sane entries', () => {
  const result = buildDesktopBackendPath({
    ruslanHome: '/Users/test/.ruslan',
    venvRoot: '/Users/test/.ruslan/ruslan-agent/venv',
    currentPath: '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin',
    platform: 'darwin',
    pathModule: path.posix
  })

  const entries = result.split(':')
  assert.equal(entries[0], '/Users/test/.ruslan/node/bin')
  assert.equal(entries[1], '/Users/test/.ruslan/ruslan-agent/venv/bin')
  assert.ok(entries.includes('/opt/homebrew/bin'), 'Apple Silicon Homebrew bin is added')
  assert.ok(entries.includes('/opt/homebrew/sbin'), 'Apple Silicon Homebrew sbin is added')
  assert.ok(entries.includes('/usr/local/sbin'), 'missing standard sbin is added')

  for (const expected of POSIX_SANE_PATH_ENTRIES) {
    assert.ok(entries.includes(expected), `${expected} should be present`)
  }
})

test('desktop backend PATH preserves first occurrence and avoids duplicates', () => {
  const result = buildDesktopBackendPath({
    ruslanHome: '/Users/test/.ruslan',
    venvRoot: '/Users/test/.ruslan/ruslan-agent/venv',
    currentPath: '/opt/homebrew/bin:/usr/bin:/opt/homebrew/bin:/bin',
    platform: 'darwin',
    pathModule: path.posix
  })

  const entries = result.split(':')
  assert.equal(entries.filter(entry => entry === '/opt/homebrew/bin').length, 1)
  assert.ok(
    entries.indexOf('/opt/homebrew/bin') < entries.indexOf('/opt/homebrew/sbin'),
    'existing Homebrew bin keeps its precedence over appended missing sane entries'
  )
})

test('buildDesktopBackendEnv extends PYTHONPATH and backend PATH together', () => {
  const env = buildDesktopBackendEnv({
    ruslanHome: '/Users/test/.ruslan',
    pythonPathEntries: ['/repo/ruslan-agent'],
    venvRoot: '/Users/test/.ruslan/ruslan-agent/venv',
    currentEnv: {
      PATH: '/usr/bin:/bin',
      PYTHONPATH: '/existing/pythonpath'
    },
    platform: 'darwin',
    pathModule: path.posix
  })

  assert.equal(env.PYTHONPATH, '/repo/ruslan-agent:/existing/pythonpath')
  assert.ok(env.PATH.startsWith('/Users/test/.ruslan/node/bin:/Users/test/.ruslan/ruslan-agent/venv/bin:'))
  assert.ok(env.PATH.includes('/opt/homebrew/bin'))
})

test('normalizeRuslanHomeRoot maps profile homes back to the global Ruslan root', () => {
  assert.equal(
    normalizeRuslanHomeRoot('/Users/test/.ruslan/profiles/oracle', { pathModule: path.posix }),
    '/Users/test/.ruslan'
  )
  assert.equal(
    normalizeRuslanHomeRoot('C:\\Users\\test\\AppData\\Local\\ruslan\\profiles\\oracle', { pathModule: path.win32 }),
    'C:\\Users\\test\\AppData\\Local\\ruslan'
  )
  assert.equal(normalizeRuslanHomeRoot('/Users/test/.ruslan', { pathModule: path.posix }), '/Users/test/.ruslan')
})

test('Windows PATH casing and delimiter are preserved without POSIX sane entries', () => {
  const env = buildDesktopBackendEnv({
    ruslanHome: 'C:\\Users\\test\\AppData\\Local\\ruslan',
    pythonPathEntries: ['C:\\repo\\ruslan-agent'],
    venvRoot: 'C:\\Users\\test\\AppData\\Local\\ruslan\\ruslan-agent\\venv',
    currentEnv: {
      Path: 'C:\\Windows\\System32;C:\\Windows',
      PYTHONPATH: 'C:\\existing\\pythonpath'
    },
    platform: 'win32',
    pathModule: path.win32
  })

  assert.equal(pathEnvKey({ Path: 'x' }, 'win32'), 'Path')
  assert.equal(env.PATH, undefined)
  assert.ok(env.Path.startsWith('C:\\Users\\test\\AppData\\Local\\ruslan\\node\\bin;'))
  assert.ok(env.Path.includes('\\venv\\Scripts;'))
  assert.ok(env.Path.includes(';C:\\Windows\\System32;C:\\Windows'))
  assert.equal(env.Path.includes('/opt/homebrew/bin'), false)
})

test('appendUniquePathEntries drops empty entries and keeps first occurrence', () => {
  assert.equal(appendUniquePathEntries([':/a::/b', ['/a', '/c']], { delimiter: ':' }), '/a:/b:/c')
})
