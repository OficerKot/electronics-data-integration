import json

import requests
from bs4 import BeautifulSoup

from parsers.model.Product import Product
from parsers.yandex.config import *
from parsers.yandex.product_details import parse_characteristics, extract_image_url, extract_source_id
from utils.brand_model import extract_brand_model

from utils.date import extract_date_parsed
from utils.html_helpers import get_text, get_url
from utils.json_storage import save_products
from utils.price import parse_price


def parse_zone_data(card):
    """Читает дополнительные данные из JSON внутри карточки."""
    raw_data = card.get("data-zone-data")

    if not raw_data:
        return {}

    try:
        return json.loads(raw_data)
    except (json.JSONDecodeError, TypeError):
        return {}


def parse_product_card(card, category):
    """Преобразует одну карточку Яндекс Маркета в Product."""

    name = get_text(card, ITEM_SELECTORS["name"])
    price_text = get_text(card, ITEM_SELECTORS["price"])
    url = get_url(card, ITEM_SELECTORS["url"], BASE_URL)

    if not name or not url:
        return None

    # Дополнительные структурированные данные Яндекса
    zone_data = parse_zone_data(card)
    characteristics = parse_characteristics(card)
    image_url = extract_image_url(card)
    date_parsed = extract_date_parsed()
    source_id = extract_source_id(url)
    brand, model = extract_brand_model(name)

    return Product(
        source="Yandex Market",
        category=category,
        name=name,
        price=parse_price(price_text),
        url=url,
        source_id=source_id,
        brand = brand,
        model = model,
        description=zone_data.get("description"),
        characteristics=characteristics,
        date_parsed=date_parsed,
        image_url=image_url
    )

def get_page(session, url: str, page: int):
    try:
        response = session.get(
            url,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Не удалось загрузить страницу: {error}")

    return BeautifulSoup(response.content, "html.parser")

def parse_url():
    products = []
    seen_urls = set()

    with requests.Session() as session:
        for category, category_url in CATEGORY_URLS.items():
            print("\n" + "=" * 60)
            print(f"Категория: {category}")

            for i in range(1, MAX_PAGES+1):

                soup = get_page(session, category_url, i)
                cards = soup.select(CARD_SELECTOR)

                print(f"Страница {i},карточек найдено: {len(cards)}")

                for card in cards:
                    product = parse_product_card(card, category)

                    if product is None:
                        continue

                    if product.url in seen_urls:
                        continue

                    seen_urls.add(product.url)
                    products.append(product)

    save_products(products, "yandex_market_products.json")

    print(f"\nВсего товаров: {len(products)}")

parse_url()