
import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import *
from parsers.model.Product import Product
from parsers.rbt.product_details import extract_description, extract_characteristics, extract_price, extract_image_url
from parsers.yandex.product_details import extract_brand_model
from utils.date import extract_date_parsed
from utils.json_storage import save_products
from utils.price import parse_price


# 1. Загрузка страницы каталога

def get_page(session, url, page):
    """Загружает страницу категории и возвращает BeautifulSoup."""

    try:
        response = session.get(
            url,
            params={"page": page},
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Ошибка загрузки страницы: {error}")
        return None

    return BeautifulSoup(response.content, "html.parser")


# 2. Поиск карточек товаров

def get_product_cards(soup):
    """Находит карточки товаров на странице."""

    cards = soup.select(CARD_SELECTOR)

    return cards


# 3. Обработка одной карточки товара

def parse_product_card(card, category):
    """Преобразует HTML-карточку в объект Product."""

    # ID товара
    product_id = card.get("data-item-id")

    if not product_id:
        return None

    # Название
    title_element = card.select_one(NAME_SELECTOR)

    if title_element is None:
        return None

    name = title_element.get_text(" ", strip=True)

    # Ссылка
    href = title_element.get("href")

    if not href:
        return None

    url = urljoin(BASE_URL, href)

    price = extract_price(card)
    description = extract_description(card)
    characteristics = extract_characteristics(card)
    img_url = extract_image_url(card)
    date_parsed = extract_date_parsed()
    brand, model = extract_brand_model(name)
    # Создаём объект товара
    return Product(
        source="RBT",
        category=category,
        source_id=product_id,
        name=name,
        price=price,
        url=url,
        description=description,
        brand=brand,
        model=model,
        characteristics=characteristics,
        image_url=img_url,
        date_parsed=date_parsed
    )


# 6. Обработка одной категории

def parse_category(session, category, category_url, seen_ids):
    """Собирает товары со всех доступных страниц категории."""

    products = []
    seen_in_category = set()

    for page in range(1, MAX_PAGES + 1):

        print(f"\nКатегория: {category} | Страница: {page}")

        soup = get_page(session, category_url, page)

        if soup is None:
            print("Не удалось загрузить страницу.")
            break

        print(f"URL: {category_url}")

        # Находим карточки
        cards = get_product_cards(soup)

        print(f"Карточек найдено: {len(cards)}")

        if not cards:
            print("Карточек нет. Остановка.")
            break

        added = 0

        for card in cards:

            product = parse_product_card(card, category)

            if product is None:
                continue

            product_id = product.source_id

            # Проверяем повторы внутри категории
            if product_id in seen_in_category:
                continue

            seen_in_category.add(product_id)
            added += 1

            # Проверяем повторы среди всех категорий
            if product_id in seen_ids:
                continue

            seen_ids.add(product_id)
            products.append(product)

        print(f"Новых товаров добавлено: {added}")

        # Если страница полностью повторяется
        if added == 0:
            print("Новых товаров нет. Останавливаемся.")
            break

    return products


# 7. Запуск всех категорий

def parse_all_categories():
    """Последовательно обрабатывает все категории RBT."""

    all_products = []
    seen_ids = set()

    with requests.Session() as session:

        for category, category_url in CATEGORY_URLS.items():

            print("\n" + "=" * 60)
            print(f"КАТЕГОРИЯ: {category}")

            products = parse_category(
                session,
                category,
                category_url,
                seen_ids
            )

            all_products.extend(products)

            # Сохраняем после каждой категории
            save_products(all_products, JSON_NAME)

            print(f"Товаров в категории: {len(products)}")
            print(f"Всего собрано: {len(all_products)}")

    return all_products


# Запуск парсера

if __name__ == "__main__":

    products = parse_all_categories()

    save_products(products, JSON_NAME)

    print("\n" + "=" * 60)
    print(f"Всего уникальных товаров: {len(products)}")
    print(f"Данные сохранены в {JSON_NAME}")
