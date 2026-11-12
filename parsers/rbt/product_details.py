import json
from datetime import datetime
from urllib.parse import urljoin

from parsers.rbt.config import PRICE_SELECTOR, CHARACTERISTICS_SELECTOR, IMAGE_SELECTOR, BASE_URL
from utils.price import parse_price


def extract_characteristics(card):
    """Собирает характеристики товара."""

    characteristics = []
    elements = card.select_one(CHARACTERISTICS_SELECTOR)
    for element in elements:
        text = element.get_text(" ", strip=True)
        if text:
            if ':' in text:
                name, value = text.split(':', 1)
                characteristics.append({
                    "name": name.strip(),
                    "value": value.strip()
                })
            else:
                characteristics.append({
                    "name": None,
                    "value": text.strip()
                })
    return characteristics


# 4. Извлечение описания из JSON-LD

def extract_description(card):
    """Получает описание товара из JSON-LD."""

    script = card.select_one(
        'script[type="application/ld+json"]'
    )

    if script is None:
        return None

    try:
        data = json.loads(script.get_text(strip=True))

    except (json.JSONDecodeError, TypeError):
        return None

    if isinstance(data, dict):
        return data.get("description")

    return None

def extract_price(card):
    price_element = card.select_one(PRICE_SELECTOR)

    price_text = (
        price_element.get_text(" ", strip=True)
        if price_element else None
    )

    return parse_price(price_text)

def extract_image_url(card):
    """Получает настоящую ссылку на изображение товара."""
    image_element = card.select_one(IMAGE_SELECTOR)

    if image_element is None:
        return None

    image_url = (
        image_element.get("data-src")
        or image_element.get("data-original")
        or image_element.get("src")
    )
    image_url = image_url.split("#")[0]

    return urljoin(BASE_URL, image_url)



