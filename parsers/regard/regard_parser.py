
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from parsers.model.Product import Product
from parsers.regard.config import *
from parsers.regard.product_details import *
from utils.date import extract_date_parsed
from utils.html_helpers import get_text
from utils.json_storage import save_products
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def parse_main_product(card, category):
    """Извлекает данные основной карточки."""

    title_element = card.select_one(".CardText_title__gGZc5")
    link = card.select_one("a.CardText_link__ny3N2[href]")

    if title_element is None or link is None:
        return None

    name = title_element.get_text(" ", strip=True)
    url = urljoin(BASE_URL, link["href"])

    brand = extract_brand(name)
    model = get_model(name, brand)
    source_id = get_source_id(url)
    description = get_text(
        card,
        ".CardText_text__9MCH8"
    )
    price = extract_price(card)
    characteristics = parse_characteristics(description)
    image_url = extract_image_url(card)
    date_parsed = extract_date_parsed()

    return Product(
        source="Regard",
        category=category,
        source_id=source_id,
        name=name,
        url=url,
        price=price,
        description=description,
        brand=brand,
        model=model,
        characteristics=characteristics,
        date_parsed=date_parsed,
        image_url=image_url
    )



def parse_variant(variant, category):
    """Извлекает данные одной модификации."""

    link = variant.select_one(
        "a.SimilarGood_title__bt0RM[href]"
    )

    if link is None:
        return None

    name = link.get_text(" ", strip = True)
    url = urljoin(BASE_URL, link["href"])

    description = get_text(
        variant.select_one(".SimilarGood_brief__vqsSI")
    )

    # Определяем бренд, модель и ID
    brand = extract_brand(name)
    model = get_model(name, brand)
    source_id = get_source_id(url)
    price = extract_price(variant)
    characteristics = parse_characteristics(description)
    date_parsed = extract_date_parsed()
    image_url = extract_image_url(variant)
    return Product(
        source="Regard",
        category=category,
        source_id=source_id,
        name=name,
        url=url,
        price=price,
        description=description,
        brand=brand,
        model=model,
        characteristics=characteristics,
        date_parsed = date_parsed,
        image_url = image_url
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
            response = get_with_backoff(
                session,
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

def get_with_backoff(session, url, max_retries=3, **kwargs):
    """Загружает страницу с обработкой ограничения 429."""

    for attempt in range(max_retries):

        response = session.get(url, **kwargs)

        if response.status_code != 429:
            response.raise_for_status()
            return response

        # Считываем рекомендованное время ожидания
        retry_after = response.headers.get("Retry-After")

        if retry_after:
            try:
                delay = float(retry_after)

            except ValueError:
                try:
                    retry_date = parsedate_to_datetime(retry_after)

                    if retry_date.tzinfo is None:
                        retry_date = retry_date.replace(
                            tzinfo=timezone.utc
                        )

                    delay = max(
                        0,
                        (retry_date - datetime.now(timezone.utc)).total_seconds()
                    )

                except (ValueError, TypeError, OverflowError):
                    delay = 60 * (2 ** attempt)

        else:
            # Если сайт не сообщил время ожидания
            delay = 60 * (2 ** attempt)

        if attempt == max_retries - 1:
            print("Повторный 429. Останавливаем сбор.")
            return None

        print(f"Получен 429. Ожидание {delay:.0f} секунд...")
        time.sleep(delay)

    return None

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