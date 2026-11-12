from urllib.parse import urljoin

from parsers.yandex.config import ITEM_SELECTORS, BASE_URL



from urllib.parse import urljoin

from parsers.yandex.config import BASE_URL
from urllib.parse import urlparse

import re

def extract_brand_model(name):
    if not name:
        return None, None

    words = name.split()

    # Ищем первое слово на английском языке
    brand_index = None

    for i, word in enumerate(words):
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", word):
            brand_index = i
            break

    if brand_index is None:
        return None, None

    brand = words[brand_index].strip(".,()[]")

    # Следующее слово считаем моделью
    model = None

    if brand_index + 1 < len(words):
        model = words[brand_index + 1].strip(".,()[]")

    return brand, model

def extract_source_id(url):
    path = urlparse(url).path.rstrip("/")
    return path.split("/")[-1] or None

def parse_characteristics(card):
    """Извлекает характеристики товара из карточки."""
    characteristics = []

    for element in card.select(".B_ssj"):
        spans = element.select("span")

        if len(spans) < 2:
            continue

        name = spans[0].get_text(" ", strip=True).rstrip(":")
        value = spans[1].get_text(" ", strip=True)

        if name and value:
            characteristics.append({
                "name": name,
                "value": value
            })

    return characteristics


def extract_image_url(card):
    """Извлекает изображение товара."""
    image = card.select_one('img[src*="avatars.mds.yandex.net"]')

    if image is None:
        return None

    image_url = image.get("src")

    if not image_url:
        return None

    return urljoin(BASE_URL, image_url.split("#")[0])
