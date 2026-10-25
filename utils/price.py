def parse_price(price_text: str | None) -> int | None:
    """Преобразует текст цены в число."""

    if not price_text:
        return None

    digits = "".join(
        char for char in price_text
        if char.isdigit()
    )

    return int(digits) if digits else None