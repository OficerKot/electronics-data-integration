
import json
from pathlib import Path
from datetime import datetime
from decimal import Decimal, InvalidOperation

from database.connection import get_connection


BASE_DIR = Path(__file__).resolve().parent.parent

JSON_FILES = [
    BASE_DIR / "data" / "yandex_market_products.json",
    BASE_DIR / "data" / "rbt_products.json",
    BASE_DIR / "data" / "regard_products.json"
]


def load_json(path):
    """Загружает данные из JSON."""

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Поддерживаем как обычный список, так и объект с ключом products
    if isinstance(data, dict):
        data = data.get("products", [])

    return data


def get_or_create_product(cursor, item):
    """Находит товар или создаёт новый."""

    sql_select = """
        SELECT id
        FROM products
        WHERE name = %s
        AND brand <=> %s
        AND model <=> %s
        LIMIT 1
    """

    cursor.execute(
        sql_select,
        (item["name"], item.get("brand"), item.get("model"))
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    sql_insert = """
        INSERT INTO products (
            name,
            description,
            brand,
            model,
            image_url
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql_insert,
        (
            item["name"],
            item.get("description"),
            item.get("brand"),
            item.get("model"),
            item.get("image_url")
        )
    )

    return cursor.lastrowid


def import_attributes(cursor, product_id, characteristics):
    """Добавляет характеристики товара."""

    sql = """
        INSERT INTO attributes (
            product_id,
            attribute_name,
            attribute_value
        )
        VALUES (%s, %s, %s)
    """

    for attr in characteristics:
        name = attr.get("name")
        value = attr.get("value")

        if not value:
            continue

        # Проверяем, чтобы повторный импорт
        # не создавал одинаковые характеристики.
        cursor.execute(
            """
            SELECT id FROM attributes
            WHERE product_id = %s
            AND attribute_name <=> %s
            AND attribute_value = %s
            LIMIT 1
            """,
            (product_id, name, value)
        )

        if not cursor.fetchone():
            cursor.execute(sql, (product_id, name, value))


def import_offer(cursor, product_id, item):
    """Добавляет или обновляет предложение магазина."""

    price = item.get("price")

    if price is not None:
        try:
            price = Decimal(str(price))
        except InvalidOperation:
            price = None

    source = item.get("source", "Unknown")
    source_id = item.get("source_id")

    sql = """
        INSERT INTO offers (
            product_id,
            website_name,
            price,
            date_parsed,
            source_id
        )
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            product_id = VALUES(product_id),
            price = VALUES(price),
            date_parsed = VALUES(date_parsed)
    """

    cursor.execute(
        sql,
        (
            product_id,
            source,
            price,
            datetime.now(),
            source_id
        )
    )


def import_file(cursor, path):
    """Импортирует один JSON-файл."""

    data = load_json(path)

    print(f"\nИмпорт файла: {path.name}")

    imported = 0

    for item in data:
        product_id = get_or_create_product(cursor, item)

        import_attributes(
            cursor,
            product_id,
            item.get("characteristics", [])
        )

        import_offer(cursor, product_id, item)

        imported += 1

    print(f"Обработано товаров: {imported}")


def main():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        for path in JSON_FILES:
            if not path.exists():
                print(f"Файл не найден: {path}")
                continue

            import_file(cursor, path)

        connection.commit()

        print("\nИмпорт успешно завершён!")

    except Exception as error:
        connection.rollback()
        print(f"\nОшибка импорта: {error}")
        raise

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()
