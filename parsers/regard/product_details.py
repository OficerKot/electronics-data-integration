import re
from urllib.parse import urljoin
from parsers.regard.config import BASE_URL, IMAGE_SELECTOR
from utils.html_helpers import get_text
from utils.price import parse_price

product_types = (
        "Смартфон ",
        "Планшет ",
        "Ноутбук ",
        "Смарт-часы ",
        "Умные часы ",
        "Фитнес-браслет",
        "Наушники",
        "Телевизор",
        "Монитор",
        "Компьютер",
        "Моноблок"
    )

def get_model(name, brand):
    """Извлекает название модели из полного названия товара."""

    if not name or not brand:
        return None

    model = name.strip()

    for product_type in product_types:
        if model.lower().startswith(product_type.lower()):
            model = model[len(product_type):]
            break

    # Убираем бренд
    if model.lower().startswith(brand.lower()):
        model = model[len(brand):].strip()

    # Убираем код модели в скобках в конце названия
    model = re.sub(r"\s*\([A-Z0-9-]{4,}\)$", "", model)

    # Убираем информацию о памяти и всё, что идёт после неё
    model = re.split(
        r"\b\d+\s*/\s*\d+\s*(?:GB|ГБ)\b",
        model,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    return model.strip() or None

def get_model_code(name):
    """Извлекает код модели из названия товара."""

    if not name:
        return None

    match = re.search(r"\(([A-Z0-9-]{4,})\)\s*$", name)

    return match.group(1) if match else None

def get_source_id(url):
    """Извлекает ID товара из ссылки Regard."""

    if not url:
        return None

    match = re.search(r"/product/(\d+)(?:/|$)", url)

    return match.group(1) if match else None

def extract_brand(name):
    """Пытается извлечь бренд из названия товара."""
    prefixes = (
        "Смартфон ",
        "Планшет ",
        "Ноутбук ",
        "Смарт-часы ",
        "Умные часы ",
    )

    for prefix in prefixes:
        if name.lower().startswith(prefix.lower()):
            remaining_name = name[len(prefix):].strip()

            if remaining_name:
                return remaining_name.split()[0]

    return None

def extract_price(card):

    price_text = get_text(
        card,
        ".SimilarGood_price__3UBK3")
    return parse_price(price_text)

def parse_characteristics(description):
    """Преобразует строку характеристик в список."""

    if not description:
        return []

    return [
        {
            "name": None,
            "value": item.strip()
        }
        for item in description.split(",")
        if item.strip()
    ]

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
