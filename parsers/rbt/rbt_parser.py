import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import *
from utils.json_storage import save_products
from utils.price import parse_price

products = []

with requests.Session() as session:

    for category, default_url in CATEGORY_URLS.items():
        print("\n" + "=" * 60)
        print(f"КАТЕГОРИЯ: {category}")

        seen_ids = set()

        for page in range(1, MAX_PAGES + 1):
            try:
                response = session.get(
                    default_url,
                    params={"page": page},
                    headers=HEADERS,
                    timeout=15
                )
                response.raise_for_status()

            except requests.RequestException as error:
                print(f"Ошибка загрузки: {error}")
                break

            soup = BeautifulSoup(response.content, "html.parser")

            print(f"\nСтраница: {page}")
            print(f"URL: {response.url}")

            # 1. Проверяем сообщение об отсутствии товаров
            empty_message = soup.select_one(EMPTY_MSG_SELECTOR)

            if empty_message:
                break

            # 2. Находим основной контейнер каталога
            catalog = soup.select_one(CATALOG_SELECTOR)

            if catalog is None:
                break

            # 3. Ищем карточки ТОЛЬКО внутри каталога
            cards = catalog.select("aside[data-item-id]")

            if not cards:
                print("Карточек каталога нет. Остановка.")
                break

            added = 0

            # 4. Извлекаем данные из каждой карточки
            for card in cards:
                product_id = card.get("data-item-id")

                if not product_id or product_id in seen_ids:
                    continue

                seen_ids.add(product_id)

                title_element = card.select_one(ITEM_SELECTOR)
                price_element = card.select_one(PRICE_SELECTOR)
                link_element = card.select_one("a[href]")

                name = (
                    title_element.get_text(" ", strip=True)
                    if title_element else None
                )

                price = parse_price(
                    price_element.get_text(" ", strip=True)
                    if price_element else None
                )

                url = (
                    urljoin(BASE_URL, link_element["href"])
                    if link_element else None
                )

                product = {
                    "source": "RBT",
                    "category": category,
                    "source_id": product_id,
                    "name": name,
                    "price": price,
                    "url": url,
                    "description": None,
                    "brand": None,
                    "model": None,
                    "characteristics": {}
                }

                products.append(product)
                added += 1

            print(f"Карточек найдено: {len(cards)}")
            print(f"Новых товаров добавлено: {added}")

            # 5. Если товары полностью повторились,
            # вероятно, следующая страница не загрузилась
            if added == 0:
                print("Новых товаров нет. Останавливаемся.")
                break


save_products(products, JSON_NAME)
print(f"\nВсего уникальных товаров: {len(products)}")
print("Данные сохранены в rbt_products.json")

