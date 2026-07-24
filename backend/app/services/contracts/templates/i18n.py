DEFAULT_LOCALE = "es"
SUPPORTED_LOCALES = ("es", "en")


def pick(texts: dict[str, str], locale: str) -> str:
    """Devuelve el texto en `locale`, o el default (es) si el locale pedido
    no esta traducido para ese texto puntual."""
    return texts.get(locale, texts[DEFAULT_LOCALE])
