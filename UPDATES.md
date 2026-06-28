# Обновления Ruslan Agent

## Источник обновлений

**Форк:** https://github.com/valldun1/ruslan

Все обновления берутся из форка `valldun1/ruslan`, не из upstream `nousresearch/hermes-agent`.

### Git remote

```bash
$ git remote -v
origin  https://github.com/valldun1/ruslan.git (fetch)
origin  https://github.com/valldun1/ruslan.git (push)
```

## Как обновить

### Способ 1: git pull (если установлен через git clone)

```bash
cd ~/Руслан
git pull origin master
```

### Способ 2: pip (если установлен через pipx/pip)

```bash
pip install --upgrade ruslan-agent
# или
uv tool upgrade ruslan-agent
```

### Способ 3: Docker

```bash
docker pull valldun1/ruslan:latest
```

### Способ 4: Homebrew

```bash
brew upgrade ruslan-agent
```

## Автоматическая проверка обновлений

Ruslan **автоматически** проверяет наличие обновлений при запуске:

```
⚠ отстаёт на 1 коммит — выполните ruslan update для обновления
```

Эта проверка использует `git fetch` против `origin/master` (т.е. наш форк).

## Вклад в проект

PR в upstream `nousresearch/hermes-agent` — опционально. Основной форк для пользователей Руслана — **этот репозиторий** (`valldun1/ruslan`).

При создании PR в upstream учитывайте:
- Ruslan-специфичные изменения (i18n, branding) могут не подходить upstream
- Сохраняйте совместимость с английской локалью (default EN)
- Smoke-тесты: `python3 ruslan_cli/tests/test_locales.py`
