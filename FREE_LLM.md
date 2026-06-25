# 🔑 Как подключить LLM к Руслану — бесплатно

**Четыре способа запустить ИИ-агента. От «без ключа и регистрации» до «одна регистрация».**

---

## 🦙 Способ 1: Ollama — ЛОКАЛЬНО, БЕЗ КЛЮЧА (рекомендуем)

**Лучший для десктопа.** Модель работает прямо на твоём компьютере. Никаких регистраций, ключей, интернета. Полная приватность.

### Установка (3 шага)

**Шаг 1:** Установи Ollama с [ollama.com/download](https://ollama.com/download)
```bash
# Mac:
brew install ollama

# Linux:
curl -fsSL https://ollama.com/install.sh | sh
```

**Шаг 2:** Скачай модель с хорошим русским (1.5 ГБ)
```bash
ollama pull qwen2.5:1.5b
```
Другие варианты: `qwen2.5:7b` (4 ГБ, умнее), `deepseek-r1:1.5b` (рассуждения), `gemma3:4b` (Google)

**Шаг 3:** Настрой `config.yaml`:
```yaml
model:
  default: qwen2.5:1.5b
  provider: ollama
  base_url: http://localhost:11434/v1
  api_mode: chat_completions
```

Всё! Запускай Hermes — работает без интернета и без ключей.

> ❌ Для Android не подходит — локальная модель на телефоне слишком медленная.

---

## 🌐 Способ 2: OpenRouter :free — облако, 2 минуты

1. Зайди на [openrouter.ai/keys](https://openrouter.ai/keys)
2. Зарегистрируйся (почта + пароль, или через Google/GitHub)
3. Нажми **«Create API Key»**
4. Скопируй ключ (выглядит как `sk-or-v1-...`)

---

## Шаг 2: Выбрать модель

Бесплатные модели для старта (все с суффиксом `:free`):

| Модель | Для чего | Русский |
|--------|----------|---------|
| `qwen/qwen3-coder:free` | Код, универсальные задачи | ✅ Отличный |
| `deepseek/deepseek-r1:free` | Рассуждения, планирование | ✅ Хороший |
| `meta-llama/llama-3.3-70b:free` | Универсальный агент | ⚠️ Средний |

**Для кода и русского языка — начни с `qwen/qwen3-coder:free`.**

---

## Шаг 3: Настроить Руслан

### 🖥️ На компьютере (macOS / Linux / Windows)

В файле `config.yaml`:

```yaml
model:
  default: qwen/qwen3-coder:free
  provider: openrouter
```

И добавь ключ в `.env`:
```bash
OPENROUTER_API_KEY=sk-or-v1-твой-ключ
```

Перезапусти Hermes:
```bash
hermes gateway run --accept-hooks
```

### 📱 На Android (Termux)

В файле `~/.config/hermes/config.yaml`:

```yaml
model:
  default: qwen/qwen3-coder:free
  provider: openrouter
```

И в `~/.bashrc` добавь:
```bash
export OPENROUTER_API_KEY=sk-or-v1-твой-ключ
```

Перезапусти Termux, и Руслан сам подхватит изменения.

---

## Шаг 4: Проверить

Напиши боту:
```
/status
```

Если видишь модель `qwen/qwen3-coder:free` — всё работает! 🎉

---

## 💡 Что дальше

- Хочешь другую модель? Поменяй `default` в конфиге
- OpenRouter показывает лимиты в [личном кабинете](https://openrouter.ai/activity)
- Бесплатные модели имеют ограничения (обычно ~20 запросов/мин)
- Для продакшена подключи DeepSeek напрямую — `$2 за 1M токенов`

---

## 🆘 Не работает?

1. Проверь, что `config.yaml` лежит в `~/.hermes/` (комп) или `~/.config/hermes/` (Android)
2. Ключ должен быть БЕЗ кавычек в `.env`
3. Модель должна быть с `:free` — например `qwen/qwen3-coder:free`
4. Перезапусти Hermes после изменений
