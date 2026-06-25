"""Tests for the Nous-Ruslan-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"ruslan"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``ruslan-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "ruslan" tag namespace.

``is_nous_ruslan_non_agentic`` should only match the actual Valldun
Ruslan-3 / Ruslan-4 chat family.
"""

from __future__ import annotations

import pytest

from ruslan_cli.model_switch import (
    _RUSLAN_MODEL_WARNING,
    _check_ruslan_model_warning,
    is_nous_ruslan_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "NousResearch/Ruslan-3-Llama-3.1-70B",
        "NousResearch/Ruslan-3-Llama-3.1-405B",
        "ruslan-3",
        "Ruslan-3",
        "ruslan-4",
        "ruslan-4-405b",
        "ruslan_4_70b",
        "openrouter/ruslan3:70b",
        "openrouter/nousresearch/ruslan-4-405b",
        "NousResearch/Ruslan3",
        "ruslan-3.1",
    ],
)
def test_matches_real_nous_ruslan_chat_models(model_name: str) -> None:
    assert is_nous_ruslan_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nous Ruslan 3/4"
    )
    assert _check_ruslan_model_warning(model_name) == _RUSLAN_MODEL_WARNING


@pytest.mark.parametrize(
    "model_name",
    [
        # Kyle's local Modelfile — qwen3:14b under a custom tag
        "ruslan-brain:qwen3-14b-ctx16k",
        "ruslan-brain:qwen3-14b-ctx32k",
        "ruslan-honcho:qwen3-8b-ctx8k",
        # Plain unrelated models
        "qwen3:14b",
        "qwen3-coder:30b",
        "qwen2.5:14b",
        "claude-opus-4-6",
        "anthropic/claude-sonnet-4.5",
        "gpt-5",
        "openai/gpt-4o",
        "google/gemini-2.5-flash",
        "deepseek-chat",
        # Non-chat Ruslan models we don't warn about
        "ruslan-llm-2",
        "ruslan2-pro",
        "nous-ruslan-2-mistral",
        # Edge cases
        "",
        "ruslan",  # bare "ruslan" isn't the 3/4 family
        "ruslan-brain",
        "brain-ruslan-3-impostor",  # "3" not preceded by /: boundary
    ],
)
def test_does_not_match_unrelated_models(model_name: str) -> None:
    assert not is_nous_ruslan_non_agentic(model_name), (
        f"expected {model_name!r} NOT to be flagged as Nous Ruslan 3/4"
    )
    assert _check_ruslan_model_warning(model_name) == ""


def test_none_like_inputs_are_safe() -> None:
    assert is_nous_ruslan_non_agentic("") is False
    # Defensive: the helper shouldn't crash on None-ish falsy input either.
    assert _check_ruslan_model_warning("") == ""
