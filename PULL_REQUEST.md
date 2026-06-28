# Pull Request: Full Russian localization for Ruslan Agent CLI

## Summary

Adds complete Russian (RU) localization for the CLI:

- **215 i18n keys** (EN↔RU pairs) covering banner, welcome, /help, /tools, setup wizard, errors
- **100% coverage** of `/help` categories (5/5) and primary commands (69/69)
- **18 aliases** auto-resolve to translated primaries via regex
- **Default locale = RU** (was EN)
- **LANG=ru_RU.UTF-8** environment variable auto-detected
- **Skin system** now defers to i18n (previously skin override won)
- **16 smoke tests** (all passing) — auto-validates new commands/categories get translated

## What's translated

| Element | Before | After |
|---------|--------|-------|
| Banner — "Available Tools" | EN | **"Доступные инструменты"** |
| Banner — "and N more toolsets" | EN | **"(и ещё 9 наборов...)"** |
| Banner — "/help for commands" | EN | **"команды: /help"** |
| Banner — "N commits behind" | EN | **"⚠ отстаёт на 1 коммит — выполните ruslan update для обновления"** |
| Welcome | "Welcome to Ruslan Agent!..." | **"Добро пожаловать в Руслан!..."** |
| Goodbye | "Goodbye! ⚕" | **"До свидания! ⚕"** |
| Response label | "⚕ Ruslan" | **"⚕ Руслан"** |
| /help — categories | "Configuration", "Exit", "Info" | **"Конфигурация", "Выход", "Информация"** |
| /help — commands | EN (52%) | **RU (100%)** |
| /tools | "(^_^)/ Available Tools" | **"(^_^)/ Доступные инструменты"** |

## Architecture

### New file: `ruslan_cli/locales.py`

Central dictionary with categories:
- `cli.banner.*` — banner strings
- `cli.welcome.text` / `cli.goodbye.text` / `cli.branding.response_label`
- `cli.help.title` / `cli.help.category.*` / `cli.help.tip_*`
- `cli.cmd.<name>.description` — 87 commands (69 primary + 18 aliases)
- `cli.tools.*` / `cli.toolsets.*`
- `cli.setup.*` — 30+ setup wizard strings (helper `_t()` available)
- `cli.error.*` — common error messages
- `common.*` — universal strings

API:
- `t(key, locale=None, **kwargs)` — get string, safe fallback
- `get_locale(config=None, env=None)` — config > env > default

### Backward compatibility

`ruslan_cli/banner_i18n.py` → deprecated wrapper that re-exports from `locales.py`. Existing code continues to work.

### Skin integration fix

`ruslan_cli/skin_engine.py:get_branding()` — added `_BRANDING_I18N_MAP` so i18n wins over hardcoded skin strings (this was a real bug — welcome message was always EN even with `locale=ru`).

### /help alias resolution

`cli.py:show_help()` — when an alias is encountered, regex extracts the primary command name from `(alias for /primary)` and resolves through `t("cli.cmd.<primary>.description")`. Result: `bg` shows the description of `background` (translated), not its own EN description.

## Test coverage

`ruslan_cli/tests/test_locales.py` — 16 tests:

- ✅ Key parity EN↔RU (158 → 215 keys)
- ✅ Placeholder parity (`{n}`, `{cmd}`, `{provider}`)
- ✅ Default locale = ru
- ✅ `get_locale()` priority: config > env > default
- ✅ `t()` with placeholders
- ✅ Short-key compat (legacy `banner_i18n.t` API)
- ✅ Fallback on unknown key/locale
- ✅ **Auto-validates** all primary commands in `COMMANDS_BY_CATEGORY` have translation
- ✅ **Auto-validates** all categories have translation
- ✅ No Cyrillic in EN, no Latin-only garbage in RU

```bash
$ python3 ruslan_cli/tests/test_locales.py
✅ test_all_command_descriptions_have_translation
✅ test_all_help_categories_have_translation
... (16 total)
16 passed, 0 failed
```

## What's NOT translated (by design)

- Slash command names (`/help`, `/model`, `/new`) — these are identifiers
- Tool names (`terminal`, `read_file`)
- Toolset names (`web`, `file`)
- CLI command names (`ruslan`, `ruslan-cli`)
- Environment variable names (`OPENROUTER_API_KEY`)
- Model names (`claude-opus-4.6`)
- `logger.error()` messages (logs, not UI)
- Documentation files (separate effort)

## What's deferred

**`ruslan_cli/setup.py` (3383 lines)** — added helper `from ruslan_cli.locales import t as _t` so any string can be wrapped. Full translation is intentionally NOT done in this PR because it could break the interactive prompt flow. Will be done in a follow-up PR with careful testing.

## Files changed

| File | Status | Lines |
|------|--------|-------|
| `ruslan_cli/locales.py` | new | +28KB (215 keys) |
| `ruslan_cli/tests/test_locales.py` | new | +10KB (16 tests) |
| `ruslan_cli/skin_engine.py` | modified | +30 lines (i18n priority in branding) |
| `ruslan_cli/banner_i18n.py` | modified | deprecated wrapper |
| `ruslan_cli/banner.py` | modified | 1 line (fallback ru) |
| `ruslan_cli/setup.py` | modified | +5 lines (helper import) |
| `cli.py` | modified | +30 lines (welcome/help/tools i18n) |

## Screenshots

### Before
```
╭─ Ruslan Agent v0.17.0 (2026.6.19) · upstream ...  ─╮
│                                  Available Tools     │
│       minimax-m3 · Valldun       0 tools · 71 skills · /help for commands │
╰──────────────────────────────────────────────────────╯

Welcome to Ruslan Agent! Type your message or /help for commands.
```

### After
```
╭─ Ruslan Agent v0.17.0 (2026.6.19) · upstream ...  ─╮
│                              Доступные инструменты   │
│       minimax-m3 · Valldun       18 tools · 71 skills · команды: /help  │
│                                  ⚠ отстаёт на 1 коммит — выполните      │
│                                  ruslan update для обновления           │
╰──────────────────────────────────────────────────────╯

Добро пожаловать в Руслан! Введите сообщение или /help для списка команд.
```

## Phase-router artifacts

- `phases/00-context.md` — recon
- `phases/01-goal.md` — goals/scope
- `phases/02-plan.md` — plan
- `phases/03-done.md` — what was done
- `phases/04-review.md` — GLM-5.2 verdict (PASS_WITH_WARNINGS)
- `phases/04-prototype-test.md` — local prototype testing
- `phases/05-full-coverage.md` — expansion to 100%

## Reviewer notes

- This is a **purely additive** change for non-Russian locales (EN fallback works via `t()` and `get_locale()`)
- **No breaking changes** — `banner_i18n.t()` API preserved
- Default locale flipped to RU is the only behavioral change; users can override with `config.locale: en` or `LANG=en_US`
- 16 unit tests cover regression scenarios
- All changes tested live via `ruslan` CLI in headless mode

## Checklist

- [x] Tests pass (16/16)
- [x] Backward compatible
- [x] No new external dependencies
- [x] Code formatted (existing style)
- [x] Comments bilingual (code EN, docstrings EN)
- [x] Live tested in actual CLI
- [x] Phase artifacts documented
- [x] No changes to upstream/AGENTS.md
