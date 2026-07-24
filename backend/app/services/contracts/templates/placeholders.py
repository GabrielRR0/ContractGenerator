def value_or_placeholder(data: dict[str, str], key: str, label: str) -> str:
    """Devuelve el valor si existe, o `[label]` para el preview en vivo (datos incompletos)."""
    value = data.get(key)
    return value if value else f"[{label.lower()}]"
