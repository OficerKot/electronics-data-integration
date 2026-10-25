
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parsers.model.Product import Product
from parsers.regard.config import *
from utils.json_storage import save_products
from utils.price import parse_price


def get_text(element):
    """Получает текст HTML-элемента."""
    if element is None:
        return None

    return element.get_text(" ", strip=True)

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


def parse_main_product(card, category):
    """Извлекает данные основной карточки."""

    title_element = card.select_one(".CardText_title__gGZc5")
    link = card.select_one("a.CardText_link__ny3N2[href]")

    if title_element is None or link is None:
        return None

    name = get_text(title_element)
    url = urljoin(BASE_URL, link["href"])
    description = get_text(
        card.select_one(".CardText_text__9MCH8")
    )

    return Product(
        source="Regard",
        category=category,
        name=name,
        url=url,
        price=parse_price(
            card.select_one(".CardPrice_price__NPXiK").get_text(" ", strip=True)
        ),
        description=description,
        brand=extract_brand(name),
    )


def parse_variant(variant, category):
    """Извлекает данные одной модификации."""

    link = variant.select_one(
        "a.SimilarGood_title__bt0RM[href]"
    )

    if link is None:
        return None

    name = get_text(link)
    url = urljoin(BASE_URL, link["href"])
    description = get_text(
        variant.select_one(".SimilarGood_brief__vqsSI")
    )

    return Product(
        source="Regard",
        category=category,
        name=name,
        url=url,
        price=parse_price(
            variant.select_one(".SimilarGood_price__3UBK3")
        ),
        description=description,
        brand=extract_brand(name),
    )


def parse_listing_card(card, category):
    """Возвращает основной товар вместе с его модификациями."""

    products = []

    main_product = parse_main_product(card, category)

    if main_product is not None:
        products.append(main_product)

    # Модификации ищем только внутри текущей карточки
    variants = card.select(VARIANT_SELECTOR)

    for variant in variants:
        product = parse_variant(variant, category)

        if product is not None:
            products.append(product)

    return products


def parse_category(session, category, category_url, all_seen_urls):
    """Собирает товары одной категории со страниц каталога."""

    products = []
    seen_in_category = set()

    for page in range(1, MAX_PAGES + 1):
        print(f"\nКатегория: {category} | Страница: {page}")

        try:
            response = session.get(
                category_url,
                params={"page": page},
                headers=HEADERS,
                timeout=15,
            )
            response.raise_for_status()

        except requests.RequestException as error:
            print(f"Ошибка загрузки страницы: {error}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Берём только карточки товаров из каталога.
        cards = soup.select(CARD_SELECTOR)

        print(f"Основных карточек найдено: {len(cards)}")

        if not cards:
            print("Карточек нет.")
            break

        new_count = 0

        for card in cards:
            card_products = parse_listing_card(card, category)

            for product in card_products:
                if not product.url:
                    continue

                # Проверяем повторы внутри этой категории
                if product.url in seen_in_category:
                    continue

                seen_in_category.add(product.url)
                new_count += 1

                # Проверяем повторы среди всех категорий сайта
                if product.url in all_seen_urls:
                    continue

                all_seen_urls.add(product.url)
                products.append(product)

        print(f"Новых товаров на странице: {new_count}")

        # Если страница повторяется, прекращаем обход
        if new_count == 0:
            break

        time.sleep(REQUEST_PAUSE_TIME)

    return products

def parse_url():
    all_products = []
    all_seen_urls = set()

    with requests.Session() as session:
        for category, category_url in CATEGORY_URLS.items():
            print("\n" + "=" * 50)
            print(f"КАТЕГОРИЯ: {category}")

            products = parse_category(
                session,
                category,
                category_url,
                all_seen_urls,
            )

            all_products.extend(products)

    save_products(all_products, "regard_products.json")

    print(f"\nВсего товаров собрано: {len(all_products)}")

parse_url()