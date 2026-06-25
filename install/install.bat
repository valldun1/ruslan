@echo off
chcp 65001 >nul
:: ==============================================
:: 🇷🇺 Руслан — Установка на Windows (PowerShell)
:: ==============================================
:: Запуск:
::   PowerShell -ExecutionPolicy Bypass -File install.ps1
:: ==============================================

echo.
echo ╔═══════════════════════════════════════╗
echo ║     🇷🇺 Руслан — установка на Windows ║
echo ║     AI-агент для русскоязычных        ║
echo ╚═══════════════════════════════════════╝
echo.

:: Проверка PowerShell
where pwsh >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ✗ PowerShell 7+ не найден. Установи с https://github.com/PowerShell/PowerShell
    exit /b 1
)

:: Запускаем настоящий скрипт через PowerShell
pwsh -ExecutionPolicy Bypass -Command "& {
    $ErrorActionPreference = 'Stop'
    $Host.UI.RawUI.ForegroundColor = 'Cyan'

    Write-Host '╔═══════════════════════════════════════╗'
    Write-Host '║     🇷🇺 Руслан — установка на Windows ║'
    Write-Host '║     AI-агент для русскоязычных        ║'
    Write-Host '╚═══════════════════════════════════════╝'
    Write-Host ''

    # ── Проверка Python ──
    Write-Host '[1/5] Проверяю Python...' -ForegroundColor Yellow
    try {
        $pyVer = py -3 --version 2>&1
        Write-Host "  ✔ $($pyVer.Trim())" -ForegroundColor Green
    } catch {
        Write-Host '  ✗ Python 3 не найден. Устанавливаю...' -ForegroundColor Yellow
        try {
            winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements 2>$null
            refreshenv 2>$null
        } catch {
            Write-Host '  ✗ winget не сработал. Скачай Python вручную: https://python.org' -ForegroundColor Red
            Write-Host '    Обязательно отметь "Add Python to PATH" при установке'
            exit 1
        }
    }

    # ── Проверка Git ──
    Write-Host ''
    Write-Host '[2/5] Проверяю Git...' -ForegroundColor Yellow
    try {
        $gitVer = git --version 2>&1
        Write-Host "  ✔ $($gitVer.Trim())" -ForegroundColor Green
    } catch {
        Write-Host '  ✗ Git не найден. Устанавливаю...' -ForegroundColor Yellow
        try {
            winget install Git.Git --accept-package-agreements --accept-source-agreements 2>$null
            refreshenv 2>$null
        } catch {
            Write-Host '  ✗ winget не сработал. Скачай Git вручную: https://git-scm.com' -ForegroundColor Red
            exit 1
        }
    }

    # ── Клонирование ──
    Write-Host ''
    Write-Host '[3/5] Клонирую Руслан с GitHub...' -ForegroundColor Yellow
    $ruslanDir = Join-Path $HOME 'Руслан'
    if (Test-Path $ruslanDir) {
        Write-Host '  — Руслан уже есть, обновляю...' -ForegroundColor Cyan
        Push-Location $ruslanDir
        git pull 2>&1 | Select-Object -Last 1
        Pop-Location
    } else {
        git clone 'https://github.com/valldun1/ruslan.git' $ruslanDir 2>&1 | Select-Object -Last 1
    }

    # ── Установка ──
    Write-Host ''
    Write-Host '[4/5] Устанавливаю Руслан...' -ForegroundColor Yellow
    Push-Location $ruslanDir
    py -3 -m pip install -e . 2>&1 | Select-Object -Last 5
    Pop-Location

    # ── Конфигурация ──
    Write-Host ''
    Write-Host '[5/5] Создаю конфигурацию...' -ForegroundColor Yellow
    $hermesDir = Join-Path $HOME '.hermes'
    New-Item -ItemType Directory -Force $hermesDir | Out-Null

    $configPath = Join-Path $hermesDir 'config.yaml'
    if (-not (Test-Path $configPath)) {
        Copy-Item (Join-Path $ruslanDir 'config.yaml.example') $configPath
        Write-Host '  ✔ config.yaml создан (русский язык + скин Руслан)' -ForegroundColor Green
    } else {
        Write-Host '  — config.yaml уже есть, не меняю' -ForegroundColor Cyan
    }

    $soulPath = Join-Path $hermesDir 'SOUL.md'
    if (-not (Test-Path $soulPath)) {
        Copy-Item (Join-Path $ruslanDir 'SOUL.md') $soulPath
        Write-Host '  ✔ SOUL.md создан (русская персона)' -ForegroundColor Green
    } else {
        Write-Host '  — SOUL.md уже есть, не меняю' -ForegroundColor Cyan
    }

    # ── Готово ──
    Write-Host ''
    Write-Host '╔═══════════════════════════════════════╗' -ForegroundColor Green
    Write-Host '║  🇷🇺 Руслан установлен и готов!       ║' -ForegroundColor Green
    Write-Host '╚═══════════════════════════════════════╝' -ForegroundColor Green
    Write-Host ''
    Write-Host 'Что дальше:' -ForegroundColor Blue
    Write-Host '  1. Настрой провайдера:    notepad $hermesDir\config.yaml'
    Write-Host '  2. Создай .env с ключами: notepad $hermesDir\.env'
    Write-Host '  3. Запусти:               hermes gateway run --accept-hooks'
    Write-Host ''
    Write-Host 'Бесплатная LLM за 5 минут:' -ForegroundColor Blue
    Write-Host '  Регистрируйся на openrouter.ai/keys (карта не нужна)'
    Write-Host "  Подробнее: type $ruslanDir\FREE_LLM.md"
}"
