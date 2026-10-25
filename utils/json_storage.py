import json
from dataclasses import asdict
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def save_products(products, filename):
    """Сохраняет список товаров в JSON."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = [asdict(product) for product in products]

    filepath = DATA_DIR / filename

    with filepath.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"Сохранено товаров: {len(products)}")
    print(f"Файл: {filepath}")