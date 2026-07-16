# Langfuse Observability Plugin

This plugin ships bundled with Ruslan but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

Pick one:

```bash
# Interactive: walks you through credentials + SDK install + enable
ruslan tools  # → Langfuse Observability

# Manual
pip install langfuse
ruslan plugins enable observability/langfuse
```

## Required credentials

Set these in `~/.ruslan/.env` (or via `ruslan tools`):

```bash
RUSLAN_LANGFUSE_PUBLIC_KEY=pk-lf-...
RUSLAN_LANGFUSE_SECRET_KEY=sk-lf-...
RUSLAN_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
ruslan plugins list                 # observability/langfuse should show "enabled"
ruslan chat -q "hello"              # then check Langfuse for a "Ruslan turn" trace
```

## Optional tuning

```bash
RUSLAN_LANGFUSE_ENV=production       # environment tag
RUSLAN_LANGFUSE_RELEASE=v1.0.0       # release tag
RUSLAN_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
RUSLAN_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
RUSLAN_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
ruslan plugins disable observability/langfuse
```
