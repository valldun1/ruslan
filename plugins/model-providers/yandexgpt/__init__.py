"""YandexGPT provider profile.

YandexGPT is Yandex Cloud's LLM with strong Russian language support.
OpenAI-compatible API at: https://llm.api.cloud.yandex.net/foundationModels/v1

Authentication: ``Authorization: Api-Key <key>`` header.
Models: yandexgpt-pro (best quality), yandexgpt-lite (fast/cheap).
"""

from providers import register_provider
from providers.base import ProviderProfile

yandexgpt = ProviderProfile(
    name="yandexgpt",
    aliases=("yagpt", "yandex-gpt", "yandex"),
    env_vars=("YANDEX_API_KEY", "YC_API_KEY"),
    display_name="YandexGPT",
    description="Яндекс — YandexGPT Pro/Lite, отличный русский язык",
    signup_url="https://cloud.yandex.ru/services/yandexgpt",
    base_url="https://llm.api.cloud.yandex.net/foundationModels/v1",
    fallback_models=(
        "yandexgpt-pro",
        "yandexgpt-lite",
    ),
)

register_provider(yandexgpt)
