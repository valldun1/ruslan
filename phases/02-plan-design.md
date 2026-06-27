# План Android APK «Руслан» — с дизайном

## Брендинг «Руслан Agent»

**Персонаж:** Воин с бородой, молния в руке, светящиеся голубые глаза
**Символ:** Геометрический узел (как на броне)
**Шрифт:** «RUSLAN» — серебристый serif, «AGENT» — cyan sans-serif

**Иконки:**
- Квадрат с скруглением (adaptive icon)
- Круглая (для notifications)
- Superellipse (как на iOS)

**Цветовая схема
```xml
<color name="bg_primary">#0a0e1a</color>
<color name="bg_card">#161b22</color>
<color name="accent_cyan">#00d4ff</color>
<color name="text_primary">#ffffff</color>
<color name="text_secondary">#8b949e</color>
<color name="success_green">#3fb950</color>
<color name="error_red">#ff4757</color>
<color name="warning_purple">#8b5cf6</color>
```

## Экраны и layout-файлы

### 1. activity_main.xml (Dashboard)
- Header: Menu + Notification bell
- Status bar: 🟢 Активен | Gateway запущен
- Profile card: Avatar (бородатый воин с молнией), "Руслан", "AI-агент", "DeepSeek v4 Flash"
- Stats: Сессий 12 | Память 85% | Время 3д 7ч
- Buttons: "Открыть чат" (cyan), "Настройки" (secondary)
- Bottom nav: Главная | Чат | Сценарии | Профиль

### 2. activity_chat.xml
- Header: Back, Avatar + "Руслан" + "AI-агент • Активен"
- Messages RecyclerView:
  - User: right-aligned, #1a3a5c bg
  - Agent: left-aligned, #2a2d35 bg, avatar
  - Code blocks: monospace, dark bg
- Input: Attachment | Text field | Mic | Send (cyan)

### 3. activity_settings.xml
- Grouped sections (iOS-style):
  - МОДЕЛЬ: Провайдер, Модель
  - ОБЩИЕ: Язык (Ru), Telegram, Голос (STT)
  - ВНЕШНИЙ ВИД: Оформление
  - ПОВЕДЕНИЕ: Автозапуск Gateway (toggle), Уведомления (toggle)
  - ИНФОРМАЦИЯ: О приложении, Системная информация

### 4. wizard_step_1..4.xml
- Step indicator (1-2-3-4 connected)
- Step 1: Welcome + checklist
- Step 2: Provider list (DeepSeek selected)
- Step 3: API Key input (masked)
- Step 4: Telegram token + users

### 5. Custom notification layout
- Expanded: Avatar, "Руслан работает", "Gateway запущен", Stop/Restart buttons
- Collapsed: Compact version

## Drawable ресурсы (SVG/XML)
- `ic_ruslan_avatar.xml` (бородатый воин с молнией, голубые глаза)
- `ic_ruslan_symbol.xml` (геометрический узел как на броне)
- `bg_glass_card.xml` (glassmorphism)
- `btn_primary_cyan.xml`, `btn_secondary.xml`
- `ic_gateway.xml`, `ic_status_*.xml`
- Bottom nav icons

## Kotlin классы
- MainActivity.kt — Dashboard + bottom nav
- ChatActivity.kt — RecyclerView adapter для сообщений
- SettingsActivity.kt — PreferenceFragmentCompat
- SetupWizardActivity.kt — ViewPager2 + 4 фрагмента
- GatewayService.kt — ForegroundService + notification
- NotificationHelper.kt — custom notification builder
- ThemeManager.kt — dark/light/theme switching

## Требования к assets
- Avatar PNG/SVG разных размеров (72dp, 96dp, 144dp)
- Fonts: Roboto или Inter (sans-serif)
- Icons: Material Design 3 + кастомные

## GitHub Actions workflow
Тот же, что в основном плане, но с дополнительным шагом:
- Проверка lint для XML layouts
- Скриншот-тесты (если есть эмулятор)
