"""Полная локализация Ruslan Agent CLI.

Единый словарь RU/EN для всех пользовательских строк:
- баннер приветствия
- /help (категории + описания команд)
- /tools заголовки
- приветствие при старте
- setup-визард
- общие ошибки

Использование:
    from ruslan_cli.locales import t
    text = t("cli.banner.available_tools", locale="ru")

Локаль по умолчанию: "ru" (русский). EN — fallback.
Локаль можно переопределить через config.locale или LANG env.

Стиль перевода:
- Slash-команды (/help, /model), имена тулзов, CLI-команды — НЕ переводятся
- Идентификаторы (room_id, session_key) — НЕ переводятся
- Метки, приглашения, описания, ошибки — переводятся
- Бренды (Hermes) — заменены на Ruslan/Руслан по контексту
"""

from __future__ import annotations

from typing import Any

# Доступные локали. Если в конфиге указана локаль, которой нет —
# fallback на локаль по умолчанию (DEFAULT_LOCALE = "ru").
SUPPORTED_LOCALES = ("ru", "en")
DEFAULT_LOCALE = "ru"

# ============================================================================
# СЛОВАРЬ ПЕРЕВОДОВ
# ============================================================================

STRINGS: dict[str, dict[str, str]] = {
    # ========================================================================
    # ENGLISH
    # ========================================================================
    "en": {
        # --- Баннер ---
        "cli.banner.available_tools": "Available Tools",
        "cli.banner.available_skills": "Available Skills",
        "cli.banner.mcp_servers": "MCP Servers",
        "cli.banner.more_toolsets": "(and {n} more toolsets...)",
        "cli.banner.no_skills": "No skills installed",
        "cli.banner.skills_disabled": "Skills toolset disabled",
        "cli.banner.summary_help": "/help for commands",
        "cli.banner.summary_help_full": "0 tools · 71 skills · commands: /help",
        "cli.banner.summary_help_zero_tools": "{n} tools · {m} skills · commands: /help",
        "cli.banner.commits_behind_one": "⚠ 1 commit behind",
        "cli.banner.commits_behind_many": "⚠ {n} commits behind",
        "cli.banner.update_available": "⚠ update available",
        "cli.banner.update_run_cmd": " — run {cmd} to update",
        "cli.banner.commit": "commit",
        "cli.banner.commits": "commits",
        "cli.banner.tools_label": "tools",
        "cli.banner.skills_label": "skills",
        "cli.banner.commands_label": "commands",
        "cli.banner.and_n_more": "(and {n} more...)",

        # --- Приветствие ---
        "cli.welcome.text": "Welcome to Ruslan Agent! Type your message or /help for commands.",
        "cli.welcome.tip_help": "Type /help for available commands",
        "cli.welcome.starting": "Starting Ruslan Agent...",
        "cli.goodbye.text": "Goodbye! ⚔",
        "cli.branding.response_label": " ⚔ Ruslan ",

        # --- /help заголовки ---
        "cli.help.title": "Available Commands",
        "cli.help.tip_chat": "Tip: Just type your message to chat with Ruslan!",
        "cli.help.tip_multiline": "Multi-line: Alt+Enter for a new line",
        "cli.help.tip_draft": "Draft editor: Ctrl+G (Alt+G in VSCode/Cursor)",
        "cli.help.tip_paste_image": "Paste image: Alt+V (or /paste)",
        "cli.help.tip_attach_image": "Attach image: /image <path> or start your prompt with a local image path",
        "cli.help.skill_commands": "Skill Commands",
        "cli.help.skill_bundles": "Skill Bundles",
        "cli.help.quick_commands": "Quick Commands",
        "cli.help.skills_count": "({n} installed)",
        "cli.help.bundles_count": "({n} installed)",

        # --- Категории /help ---
        "cli.help.category.Setup": "Setup",
        "cli.help.category.Memory": "Memory",
        "cli.help.category.Skills": "Skills",
        "cli.help.category.Session": "Session",
        "cli.help.category.Model": "Model",
        "cli.help.category.Tools": "Tools",
        "cli.help.category.Misc": "Misc",
        "cli.help.category.Plugins": "Plugins",
        "cli.help.category.Profiles": "Profiles",
        "cli.help.category.Gateway": "Gateway",
        "cli.help.category.Dangerous": "Dangerous",
        "cli.help.category.Configuration": "Configuration",
        "cli.help.category.Exit": "Exit",
        "cli.help.category.Info": "Info",
        "cli.help.category.Tools & Skills": "Tools & Skills",
        "cli.help.category.Tools & skills": "Tools & Skills",
        "cli.help.category.Tools and skills": "Tools & Skills",

        # --- Описания команд /help ---
        "cli.cmd.help.description": "Show this help message",
        "cli.cmd.model.description": "Switch the current LLM model",
        "cli.cmd.new.description": "Start a new conversation session",
        "cli.cmd.compress.description": "Compress conversation context",
        "cli.cmd.title.description": "Set a title for the current session",
        "cli.cmd.history.description": "Browse past sessions",
        "cli.cmd.resume.description": "Resume a previous session by ID",
        "cli.cmd.tools.description": "List all available tools",
        "cli.cmd.toolsets.description": "List available toolsets",
        "cli.cmd.skills.description": "List installed skills",
        "cli.cmd.skill.description": "Show details for a specific skill",
        "cli.cmd.bundles.description": "List installed skill bundles",
        "cli.cmd.exit.description": "Exit Ruslan Agent",
        "cli.cmd.quit.description": "Exit Ruslan Agent",
        "cli.cmd.q.description": "Exit Ruslan Agent",
        "cli.cmd.workspace.description": "Show current working directory",
        "cli.cmd.cwd.description": "Show current working directory",
        "cli.cmd.paste.description": "Paste an image from clipboard",
        "cli.cmd.image.description": "Attach an image from disk",
        "cli.cmd.clear.description": "Clear the current screen",
        "cli.cmd.status.description": "Show current status (model, context, etc.)",
        "cli.cmd.config.description": "Show or edit configuration",
        "cli.cmd.setup.description": "Run the setup wizard",
        "cli.cmd.update.description": "Update Ruslan to the latest version",
        "cli.cmd.doctor.description": "Run diagnostics and check the installation",
        "cli.cmd.gateway.description": "Start the messaging gateway",
        "cli.cmd.profile.description": "Manage user profiles",
        "cli.cmd.profiles.description": "Switch between profiles",
        "cli.cmd.memory.description": "Browse or search long-term memory",
        "cli.cmd.plugins.description": "Manage installed plugins",
        "cli.cmd.bundle.description": "Show details for a skill bundle",
        "cli.cmd.reload.description": "Reload skills and plugins",
        "cli.cmd.approve.description": "Approve a pending write/exec request",
        "cli.cmd.deny.description": "Deny a pending request",
        "cli.cmd.diff.description": "Show pending file changes",
        "cli.cmd.version.description": "Show Ruslan version",
        "cli.cmd.agents.description": "Show active agents and running tasks",
        "cli.cmd.background.description": "Run a prompt in the background",
        "cli.cmd.bg.description": "Run a prompt in the background (alias for /background)",
        "cli.cmd.billing.description": "Manage Nous terminal billing — buy credits, auto-reload, limits",
        "cli.cmd.blueprint.description": "Set up an automation from a blueprint template",
        "cli.cmd.bp.description": "Set up an automation from a blueprint template (alias for /blueprint)",
        "cli.cmd.branch.description": "Branch the current session (explore a different path)",
        "cli.cmd.browser.description": "Connect browser tools to your live Chromium-family browser via CDP",
        "cli.cmd.busy.description": "Control what Enter does while Ruslan is working",
        "cli.cmd.codex-runtime.description": "Toggle codex app-server runtime for OpenAI/Codex models",
        "cli.cmd.codex_runtime.description": "Toggle codex app-server runtime for OpenAI/Codex models (alias for /codex-runtime)",
        "cli.cmd.copy.description": "Copy the last assistant response to clipboard",
        "cli.cmd.credits.description": "Show Nous credit balance and top up",
        "cli.cmd.cron.description": "Manage scheduled tasks",
        "cli.cmd.curator.description": "Background skill maintenance (status, run, pin, archive, list-archived)",
        "cli.cmd.debug.description": "Upload debug report (system info + logs) and get shareable links",
        "cli.cmd.fast.description": "Toggle fast mode — OpenAI Priority Processing / Anthropic Fast Mode",
        "cli.cmd.footer.description": "Toggle gateway runtime-metadata footer on final replies",
        "cli.cmd.goal.description": "Set a standing goal Ruslan works on across turns until achieved",
        "cli.cmd.handoff.description": "Hand off this session to a messaging platform (Telegram, Discord, etc.)",
        "cli.cmd.indicator.description": "Pick the TUI busy-indicator style",
        "cli.cmd.insights.description": "Show usage insights and analytics",
        "cli.cmd.kanban.description": "Multi-profile collaboration board (tasks, links, comments)",
        "cli.cmd.personality.description": "Set a predefined personality",
        "cli.cmd.platforms.description": "Show gateway/messaging platform status",
        "cli.cmd.prompt.description": "Compose your next prompt in $EDITOR (markdown), then send it",
        "cli.cmd.queue.description": "Queue a prompt for the next turn (doesn't interrupt)",
        "cli.cmd.reasoning.description": "Manage reasoning effort and display",
        "cli.cmd.redraw.description": "Force a full UI repaint (recovers from terminal drift)",
        "cli.cmd.reload-mcp.description": "Reload MCP servers from config",
        "cli.cmd.reload-skills.description": "Re-scan ~/.ruslan/skills/ for newly installed or removed skills",
        "cli.cmd.retry.description": "Retry the last message (resend to agent)",
        "cli.cmd.rollback.description": "List or restore filesystem checkpoints",
        "cli.cmd.save.description": "Save the current conversation",
        "cli.cmd.sessions.description": "Browse and resume previous sessions",
        "cli.cmd.skin.description": "Show or change the display skin/theme",
        "cli.cmd.snapshot.description": "Create or restore state snapshots of Ruslan config/state",
        "cli.cmd.statusbar.description": "Toggle the context/model status bar",
        "cli.cmd.steer.description": "Inject a message after the next tool call without interrupting",
        "cli.cmd.stop.description": "Kill all running background processes",
        "cli.cmd.subgoal.description": "Add or manage extra criteria on the active goal",
        "cli.cmd.suggestions.description": "Review suggested automations (accept/dismiss)",
        "cli.cmd.timestamps.description": "Toggle [HH:MM] timestamps on messages and /history",
        "cli.cmd.undo.description": "Back up N user turns and re-prompt (default 1)",
        "cli.cmd.usage.description": "Show token usage and rate limits for the current session",
        "cli.cmd.verbose.description": "Cycle tool progress display: off → new → all → verbose",
        "cli.cmd.voice.description": "Toggle voice mode",
        "cli.cmd.whoami.description": "Show your slash command access (admin / user)",
        "cli.cmd.yolo.description": "Toggle YOLO mode (skip all dangerous command approvals)",

        # --- /tools заголовки ---
        "cli.tools.title": "(^_^)/ Available Tools",
        "cli.toolsets.title": "(^_^)b Available Toolsets",
        "cli.tools.no_tools": "(;_;) No tools available",
        "cli.tools.no_toolsets": "(;_;) No toolsets available",
        "cli.tools.total": "Total: {n} tools",
        "cli.tools.toolset_label": "[{toolset}]",
        "cli.tools.total_kawaii": "Total: {n} tools  ヽ(^o^)ノ",

        # --- Setup визард: общие ---
        "cli.setup.welcome": "Welcome to Ruslan setup!",
        "cli.setup.choose_language": "Choose language / Выберите язык:",
        "cli.setup.press_enter": "Press Enter to continue...",
        "cli.setup.skip": "Skip",
        "cli.setup.back": "← Back",
        "cli.setup.next": "Next →",
        "cli.setup.done": "Done",
        "cli.setup.cancel": "Cancel",
        "cli.setup.yes": "Yes",
        "cli.setup.no": "No",
        "cli.setup.invalid_choice": "Invalid choice. Please try again.",
        "cli.setup.required": "Required",
        "cli.setup.optional": "Optional",
        "cli.setup.detected": "Detected",
        "cli.setup.not_detected": "Not detected",
        "cli.setup.already_configured": "Already configured",
        "cli.setup.not_configured": "Not configured",
        "cli.setup.ask_api_key": "Enter your API key for {provider}:",
        "cli.setup.ask_api_key_masked": "(input is hidden)",
        "cli.setup.api_key_saved": "✓ API key saved for {provider}",
        "cli.setup.api_key_invalid": "✗ Invalid API key",
        "cli.setup.ask_model": "Choose default model:",
        "cli.setup.choose_provider": "Choose LLM provider:",
        "cli.setup.testing_connection": "Testing connection...",
        "cli.setup.connection_ok": "✓ Connection successful",
        "cli.setup.connection_failed": "✗ Connection failed: {error}",
        "cli.setup.telegram_token": "Enter your Telegram bot token:",
        "cli.setup.discord_token": "Enter your Discord bot token:",
        "cli.setup.whatsapp_token": "Enter your WhatsApp Cloud API token:",
        "cli.setup.telegram_token_help": "Get it from @BotFather in Telegram",
        "cli.setup.discord_token_help": "Get it from Discord Developer Portal",
        "cli.setup.allowed_users": "Allowed user IDs (comma-separated, blank for anyone):",
        "cli.setup.admin_users": "Admin user IDs (comma-separated):",
        "cli.setup.gateway_port": "Gateway port (default 8765):",
        "cli.setup.locale": "Interface language (ru/en):",
        "cli.setup.skin": "Color scheme:",
        "cli.setup.logging_level": "Logging level:",
        "cli.setup.profile_setup": "Set up your profile",
        "cli.setup.profile_name": "Your name:",
        "cli.setup.profile_timezone": "Timezone (e.g. Europe/Moscow):",
        "cli.setup.complete": "✓ Setup complete!",
        "cli.setup.complete_subtitle": "Run 'ruslan' to start chatting",
        "cli.setup.see_docs": "See documentation: https://ruslan.team/docs",
        "cli.setup.docs_url": "https://ruslan.team/docs",
        "cli.setup.use_defaults": "Use defaults",
        "cli.setup.custom_value": "Custom value",
        "cli.setup.add_provider": "Add another provider?",
        "cli.setup.add_skill": "Install another skill?",
        "cli.setup.more_providers": "(and {n} more providers...)",

        # --- Ошибки ---
        "cli.error.unknown_command": "Unknown command: {cmd}. Type /help for available commands.",
        "cli.error.no_api_key": "No API key configured. Run 'ruslan setup' to configure.",
        "cli.error.config_not_found": "Configuration not found: {path}",
        "cli.error.file_not_found": "File not found: {path}",
        "cli.error.permission_denied": "Permission denied: {path}",
        "cli.error.network": "Network error: {error}",
        "cli.error.timeout": "Operation timed out after {n}s",
        "cli.error.cancelled": "Operation cancelled by user",
        "cli.error.invalid_input": "Invalid input: {value}",
        "cli.error.required_arg": "Required argument: {arg}",
        "cli.error.internal": "Internal error: {error}",

        # --- Универсальные ---
        "common.yes": "Yes",
        "common.no": "No",
        "common.ok": "OK",
        "common.cancel": "Cancel",
        "common.save": "Save",
        "common.loading": "Loading...",
        "common.saving": "Saving...",
        "common.error": "Error",
        "common.warning": "Warning",
        "common.success": "Success",
        "common.none": "None",
    },

    # ========================================================================
    # РУССКИЙ
    # ========================================================================
    "ru": {
        # --- Баннер ---
        "cli.banner.available_tools": "Доступные инструменты",
        "cli.banner.available_skills": "Доступные навыки",
        "cli.banner.mcp_servers": "MCP-серверы",
        "cli.banner.more_toolsets": "(и ещё {n} наборов...)",
        "cli.banner.no_skills": "Навыки не установлены",
        "cli.banner.skills_disabled": "Набор навыков отключён",
        "cli.banner.summary_help": "команды: /help",
        "cli.banner.summary_help_full": "0 инструментов · 71 навык · команды: /help",
        "cli.banner.summary_help_zero_tools": "{n} инструментов · {m} навыков · команды: /help",
        "cli.banner.commits_behind_one": "⚠ отстаёт на 1 коммит",
        "cli.banner.commits_behind_many": "⚠ отстаёт на {n} коммитов",
        "cli.banner.update_available": "⚠ доступно обновление",
        "cli.banner.update_run_cmd": " — выполните {cmd} для обновления",
        "cli.banner.commit": "коммит",
        "cli.banner.commits": "коммитов",
        "cli.banner.tools_label": "инструментов",
        "cli.banner.skills_label": "навыков",
        "cli.banner.commands_label": "команды",
        "cli.banner.and_n_more": "(и ещё {n}...)",

        # --- Приветствие ---
        "cli.welcome.text": "Добро пожаловать в Руслан! Введите сообщение или /help для списка команд.",
        "cli.welcome.tip_help": "Введите /help для списка команд",
        "cli.welcome.starting": "Запуск Руслан...",
        "cli.goodbye.text": "До свидания! ⚔",
        "cli.branding.response_label": " ⚔ Руслан ",

        # --- /help заголовки ---
        "cli.help.title": "Доступные команды",
        "cli.help.tip_chat": "Подсказка: просто напишите сообщение — Руслан ответит!",
        "cli.help.tip_multiline": "Многострочный ввод: Alt+Enter для новой строки",
        "cli.help.tip_draft": "Редактор черновика: Ctrl+G (Alt+G в VSCode/Cursor)",
        "cli.help.tip_paste_image": "Вставить картинку: Alt+V (или /paste)",
        "cli.help.tip_attach_image": "Прикрепить картинку: /image <путь> или начните промпт с локального пути",
        "cli.help.skill_commands": "Команды навыков",
        "cli.help.skill_bundles": "Наборы навыков",
        "cli.help.quick_commands": "Быстрые команды",
        "cli.help.skills_count": "(установлено {n})",
        "cli.help.bundles_count": "(установлено {n})",

        # --- Категории /help ---
        "cli.help.category.Setup": "Настройка",
        "cli.help.category.Memory": "Память",
        "cli.help.category.Skills": "Навыки",
        "cli.help.category.Session": "Сессия",
        "cli.help.category.Model": "Модель",
        "cli.help.category.Tools": "Инструменты",
        "cli.help.category.Misc": "Разное",
        "cli.help.category.Plugins": "Плагины",
        "cli.help.category.Profiles": "Профили",
        "cli.help.category.Gateway": "Шлюз",
        "cli.help.category.Dangerous": "Опасные",
        "cli.help.category.Configuration": "Конфигурация",
        "cli.help.category.Exit": "Выход",
        "cli.help.category.Info": "Информация",
        "cli.help.category.Tools & Skills": "Инструменты и навыки",
        "cli.help.category.Tools & skills": "Инструменты и навыки",
        "cli.help.category.Tools and skills": "Инструменты и навыки",

        # --- Описания команд /help ---
        "cli.cmd.help.description": "Показать эту справку",
        "cli.cmd.model.description": "Переключить текущую модель LLM",
        "cli.cmd.new.description": "Начать новую сессию разговора",
        "cli.cmd.compress.description": "Сжать контекст разговора",
        "cli.cmd.title.description": "Задать название текущей сессии",
        "cli.cmd.history.description": "Просмотреть прошлые сессии",
        "cli.cmd.resume.description": "Продолжить прошлую сессию по ID",
        "cli.cmd.tools.description": "Список всех доступных инструментов",
        "cli.cmd.toolsets.description": "Список доступных наборов инструментов",
        "cli.cmd.skills.description": "Список установленных навыков",
        "cli.cmd.skill.description": "Показать детали конкретного навыка",
        "cli.cmd.bundles.description": "Список установленных наборов навыков",
        "cli.cmd.exit.description": "Выйти из Руслана",
        "cli.cmd.quit.description": "Выйти из Руслана",
        "cli.cmd.q.description": "Выйти из Руслана",
        "cli.cmd.workspace.description": "Показать текущую рабочую папку",
        "cli.cmd.cwd.description": "Показать текущую рабочую папку",
        "cli.cmd.paste.description": "Вставить картинку из буфера обмена",
        "cli.cmd.image.description": "Прикрепить картинку с диска",
        "cli.cmd.clear.description": "Очистить экран",
        "cli.cmd.status.description": "Показать статус (модель, контекст и т.д.)",
        "cli.cmd.config.description": "Показать или изменить конфигурацию",
        "cli.cmd.setup.description": "Запустить мастер настройки",
        "cli.cmd.update.description": "Обновить Руслан до последней версии",
        "cli.cmd.doctor.description": "Запустить диагностику установки",
        "cli.cmd.gateway.description": "Запустить шлюз мессенджеров",
        "cli.cmd.profile.description": "Управление профилями пользователя",
        "cli.cmd.profiles.description": "Переключиться между профилями",
        "cli.cmd.memory.description": "Просмотр или поиск долговременной памяти",
        "cli.cmd.plugins.description": "Управление установленными плагинами",
        "cli.cmd.bundle.description": "Показать детали набора навыков",
        "cli.cmd.reload.description": "Перезагрузить навыки и плагины",
        "cli.cmd.approve.description": "Подтвердить ожидающий запрос записи/выполнения",
        "cli.cmd.deny.description": "Отклонить ожидающий запрос",
        "cli.cmd.diff.description": "Показать ожидающие изменения файлов",
        "cli.cmd.version.description": "Показать версию Руслана",
        "cli.cmd.agents.description": "Показать активных агентов и запущенные задачи",
        "cli.cmd.background.description": "Запустить промпт в фоне",
        "cli.cmd.bg.description": "Запустить промпт в фоне (алиас /background)",
        "cli.cmd.billing.description": "Управление биллингом Nous — покупка кредитов, автопополнение, лимиты",
        "cli.cmd.blueprint.description": "Настроить автоматизацию по шаблону blueprint",
        "cli.cmd.bp.description": "Настроить автоматизацию по шаблону blueprint (алиас /blueprint)",
        "cli.cmd.branch.description": "Ответвить текущую сессию (исследовать альтернативный путь)",
        "cli.cmd.browser.description": "Подключить инструменты браузера к вашему Chromium-браузеру через CDP",
        "cli.cmd.busy.description": "Что делает Enter пока Руслан работает",
        "cli.cmd.codex-runtime.description": "Переключить runtime codex app-server для моделей OpenAI/Codex",
        "cli.cmd.codex_runtime.description": "Переключить runtime codex app-server для моделей OpenAI/Codex (алиас /codex-runtime)",
        "cli.cmd.copy.description": "Скопировать последний ответ ассистента в буфер обмена",
        "cli.cmd.credits.description": "Показать баланс кредитов Nous и пополнить",
        "cli.cmd.cron.description": "Управление запланированными задачами",
        "cli.cmd.curator.description": "Фоновое обслуживание навыков (статус, запуск, закрепление, архив, список архива)",
        "cli.cmd.debug.description": "Загрузить отчёт об отладке (системная инфо + логи) и получить ссылки",
        "cli.cmd.fast.description": "Переключить быстрый режим — OpenAI Priority Processing / Anthropic Fast Mode",
        "cli.cmd.footer.description": "Показывать футер с метаданными шлюза в финальных ответах",
        "cli.cmd.goal.description": "Задать постоянную цель, над которой Руслан работает до её достижения",
        "cli.cmd.handoff.description": "Передать сессию в мессенджер (Telegram, Discord и др.)",
        "cli.cmd.indicator.description": "Выбрать стиль индикатора занятости в TUI",
        "cli.cmd.insights.description": "Показать аналитику использования",
        "cli.cmd.kanban.description": "Доска совместной работы (задачи, ссылки, комментарии) для нескольких профилей",
        "cli.cmd.personality.description": "Задать предопределённую личность",
        "cli.cmd.platforms.description": "Статус шлюза и мессенджер-платформ",
        "cli.cmd.prompt.description": "Создать следующий промпт в $EDITOR (markdown), затем отправить",
        "cli.cmd.queue.description": "Поставить промпт в очередь на следующий ход (не прерывает)",
        "cli.cmd.reasoning.description": "Управление глубиной рассуждений и их отображением",
        "cli.cmd.redraw.description": "Полная перерисовка TUI (восстановление после дрейфа терминала)",
        "cli.cmd.reload-mcp.description": "Перезагрузить MCP-серверы из конфига",
        "cli.cmd.reload-skills.description": "Пересканировать ~/.ruslan/skills/ на новые/удалённые навыки",
        "cli.cmd.retry.description": "Повторить последнее сообщение (отправить агенту заново)",
        "cli.cmd.rollback.description": "Список или восстановление чекпоинтов файловой системы",
        "cli.cmd.save.description": "Сохранить текущий разговор",
        "cli.cmd.sessions.description": "Просмотр и возобновление прошлых сессий",
        "cli.cmd.skin.description": "Показать или сменить скин/тему отображения",
        "cli.cmd.snapshot.description": "Создать или восстановить снимки состояния Руслана",
        "cli.cmd.statusbar.description": "Показывать статус-бар с контекстом/моделью",
        "cli.cmd.steer.description": "Вставить сообщение после следующего вызова инструмента без прерывания",
        "cli.cmd.stop.description": "Остановить все запущенные фоновые процессы",
        "cli.cmd.subgoal.description": "Добавить или управлять дополнительными критериями активной цели",
        "cli.cmd.suggestions.description": "Просмотр предложенных автоматизаций (принять/отклонить)",
        "cli.cmd.timestamps.description": "Показывать [HH:MM] метки времени в сообщениях и /history",
        "cli.cmd.undo.description": "Откатить N пользовательских ходов и переспросить (по умолчанию 1)",
        "cli.cmd.usage.description": "Показать использование токенов и лимиты текущей сессии",
        "cli.cmd.verbose.description": "Цикл отображения прогресса инструментов: выкл → новые → все → подробно",
        "cli.cmd.voice.description": "Переключить голосовой режим",
        "cli.cmd.whoami.description": "Показать ваш доступ к slash-командам (админ / пользователь)",
        "cli.cmd.yolo.description": "Переключить режим YOLO (пропуск всех подтверждений опасных команд)",

        # --- /tools заголовки ---
        "cli.tools.title": "(^_^)/ Доступные инструменты",
        "cli.toolsets.title": "(^_^)b Доступные наборы инструментов",
        "cli.tools.no_tools": "(;_;) Нет доступных инструментов",
        "cli.tools.no_toolsets": "(;_;) Нет доступных наборов",
        "cli.tools.total": "Всего: {n} инструментов",
        "cli.tools.toolset_label": "[{toolset}]",
        "cli.tools.total_kawaii": "Всего: {n} инструментов  ヽ(^o^)ノ",

        # --- Setup визард: общие ---
        "cli.setup.welcome": "Добро пожаловать в настройку Руслана!",
        "cli.setup.choose_language": "Choose language / Выберите язык:",
        "cli.setup.press_enter": "Нажмите Enter для продолжения...",
        "cli.setup.skip": "Пропустить",
        "cli.setup.back": "← Назад",
        "cli.setup.next": "Далее →",
        "cli.setup.done": "Готово",
        "cli.setup.cancel": "Отмена",
        "cli.setup.yes": "Да",
        "cli.setup.no": "Нет",
        "cli.setup.invalid_choice": "Неверный выбор. Попробуйте ещё раз.",
        "cli.setup.required": "Обязательно",
        "cli.setup.optional": "Необязательно",
        "cli.setup.detected": "Обнаружено",
        "cli.setup.not_detected": "Не обнаружено",
        "cli.setup.already_configured": "Уже настроено",
        "cli.setup.not_configured": "Не настроено",
        "cli.setup.ask_api_key": "Введите API-ключ для {provider}:",
        "cli.setup.ask_api_key_masked": "(ввод скрыт)",
        "cli.setup.api_key_saved": "✓ API-ключ сохранён для {provider}",
        "cli.setup.api_key_invalid": "✗ Неверный API-ключ",
        "cli.setup.ask_model": "Выберите модель по умолчанию:",
        "cli.setup.choose_provider": "Выберите провайдера LLM:",
        "cli.setup.testing_connection": "Проверка соединения...",
        "cli.setup.connection_ok": "✓ Соединение успешно",
        "cli.setup.connection_failed": "✗ Ошибка соединения: {error}",
        "cli.setup.telegram_token": "Введите токен Telegram-бота:",
        "cli.setup.discord_token": "Введите токен Discord-бота:",
        "cli.setup.whatsapp_token": "Введите токен WhatsApp Cloud API:",
        "cli.setup.telegram_token_help": "Получите его у @BotFather в Telegram",
        "cli.setup.discord_token_help": "Получите его в Discord Developer Portal",
        "cli.setup.allowed_users": "Разрешённые ID пользователей (через запятую, пусто = для всех):",
        "cli.setup.admin_users": "ID администраторов (через запятую):",
        "cli.setup.gateway_port": "Порт шлюза (по умолчанию 8765):",
        "cli.setup.locale": "Язык интерфейса (ru/en):",
        "cli.setup.skin": "Цветовая схема:",
        "cli.setup.logging_level": "Уровень логирования:",
        "cli.setup.profile_setup": "Настройка вашего профиля",
        "cli.setup.profile_name": "Ваше имя:",
        "cli.setup.profile_timezone": "Часовой пояс (например, Europe/Moscow):",
        "cli.setup.complete": "✓ Настройка завершена!",
        "cli.setup.complete_subtitle": "Запустите 'ruslan' чтобы начать общение",
        "cli.setup.see_docs": "Документация: https://ruslan.team/docs",
        "cli.setup.docs_url": "https://ruslan.team/docs",
        "cli.setup.use_defaults": "Использовать значения по умолчанию",
        "cli.setup.custom_value": "Своё значение",
        "cli.setup.add_provider": "Добавить ещё одного провайдера?",
        "cli.setup.add_skill": "Установить ещё один навык?",
        "cli.setup.more_providers": "(и ещё {n} провайдеров...)",

        # --- Ошибки ---
        "cli.error.unknown_command": "Неизвестная команда: {cmd}. Введите /help для списка команд.",
        "cli.error.no_api_key": "API-ключ не настроен. Запустите 'ruslan setup' для настройки.",
        "cli.error.config_not_found": "Конфигурация не найдена: {path}",
        "cli.error.file_not_found": "Файл не найден: {path}",
        "cli.error.permission_denied": "Доступ запрещён: {path}",
        "cli.error.network": "Ошибка сети: {error}",
        "cli.error.timeout": "Время ожидания истекло через {n}с",
        "cli.error.cancelled": "Операция отменена пользователем",
        "cli.error.invalid_input": "Неверный ввод: {value}",
        "cli.error.required_arg": "Обязательный аргумент: {arg}",
        "cli.error.internal": "Внутренняя ошибка: {error}",

        # --- Универсальные ---
        "common.yes": "Да",
        "common.no": "Нет",
        "common.ok": "ОК",
        "common.cancel": "Отмена",
        "common.save": "Сохранить",
        "common.loading": "Загрузка...",
        "common.saving": "Сохранение...",
        "common.error": "Ошибка",
        "common.warning": "Предупреждение",
        "common.success": "Успешно",
        "common.none": "Нет",
    },
}


# ============================================================================
# API
# ============================================================================

def t(key: str, locale: str | None = None, **kwargs: Any) -> str:
    """Получить локализованную строку.

    Args:
        key: ключ в формате "cli.banner.<name>" (префикс опционален)
        locale: "ru" или "en". None → дефолт (DEFAULT_LOCALE = "ru")
        **kwargs: плейсхолдеры для подстановки ({n}, {cmd}, {provider}...)

    Returns:
        Локализованная строка с подставленными плейсхолдерами.
        Если ключ не найден — возвращает сам ключ (безопасный fallback).
    """
    # Дефолт
    if locale is None:
        locale = DEFAULT_LOCALE

    # Fallback на дефолт для неизвестной локали
    if locale not in STRINGS:
        locale = DEFAULT_LOCALE

    # Обратная совместимость со старым API banner_i18n:
    # короткие ключи без префикса (e.g. "available_tools") → "cli.banner.available_tools"
    if "." not in key:
        # Это короткий ключ из старого banner_i18n API
        key = f"cli.banner.{key}"

    # Получить строку
    strings = STRINGS[locale]
    value = strings.get(key, key)

    # Подставить плейсхолдеры (если есть kwargs)
    if kwargs:
        try:
            return value.format(**kwargs)
        except (KeyError, IndexError):
            # Если плейсхолдер не передан — вернуть как есть (без падения)
            return value
    return value


def get_locale(config: dict | None = None, env: dict | None = None) -> str:
    """Определить локаль: config.locale > LANG env > DEFAULT_LOCALE.

    Args:
        config: dict конфигурации (опционально, ищем ключ 'locale')
        env: dict окружения (опционально, ищем 'LANG'/'LC_ALL')

    Returns:
        "ru" или "en"
    """
    # 1. Из конфига
    if config and isinstance(config, dict):
        cfg_locale = config.get("locale") or config.get("language")
        if cfg_locale in SUPPORTED_LOCALES:
            return cfg_locale

    # 2. Из LANG/LC_ALL
    if env:
        for env_key in ("LANG", "LC_ALL", "LANGUAGE"):
            val = env.get(env_key, "")
            if val and val.lower().startswith("ru"):
                return "ru"
            if val and val.lower().startswith("en"):
                return "en"

    # 3. Дефолт
    return DEFAULT_LOCALE


# ============================================================================
# Backward-compat: старый API из banner_i18n
# ============================================================================

def _compat_t(key: str, locale: str = "en", **kwargs: Any) -> str:
    """Обратная совместимость со старым banner_i18n.t (BANNER_STRINGS-стиль)."""
    # Старые ключи: "available_tools" (без префикса) → "cli.banner.available_tools"
    if "." not in key and not key.startswith("cli."):
        key = f"cli.banner.{key}"
    return t(key, locale=locale, **kwargs)


# Алиас для обратной совместимости
def _legacy_t(key: str, locale: str = "en", **kwargs: Any) -> str:
    """Полная обратная совместимость с banner_i18n.t."""
    return _compat_t(key, locale=locale, **kwargs)
