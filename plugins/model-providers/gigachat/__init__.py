"""GigaChat provider profile.

GigaChat is Sber's LLM with strong Russian language support.
OpenAI-compatible API at: https://gigachat.devices.sberbank.ru/api/v1

Authentication: OAuth2 token exchange. Obtain a token via:
  1. Register at https://developers.sber.ru/
  2. Exchange client credentials for access token at
     https://ngw.devices.sberbank.ru:9443/api/v2/oauth
  3. Set GIGACHAT_ACCESS_TOKEN env var to the token value

Models: GigaChat-Pro, GigaChat-Lite, GigaChat-Max.
"""

from providers import register_provider
from providers.base import ProviderProfile

gigachat = ProviderProfile(
    name="gigachat",
    aliases=("giga-chat", "giga", "sbergpt", "sber"),
    env_vars=("GIGACHAT_ACCESS_TOKEN", "GIGACHAT_API_KEY", "SBER_AUTH_KEY"),
    display_name="GigaChat",
    description="Сбер — GigaChat Pro/Lite/Max, отличный русский язык",
    signup_url="https://developers.sber.ru/",
    base_url="https://gigachat.devices.sberbank.ru/api/v1",
    fallback_models=(
        "GigaChat-Pro",
        "GigaChat-Lite",
        "GigaChat-Max",
    ),
)

register_provider(gigachat)
