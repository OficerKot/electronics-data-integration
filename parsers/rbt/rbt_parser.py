import requests
from bs4 import BeautifulSoup
from config import CATEGORY_URLS


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


for category, url in CATEGORY_URLS.items():
    print("\n" + "=" * 60)
    print(f"КАТЕГОРИЯ: {category}")
    print(f"URL: {url}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.select('div[class = "ProductLineCard_container__sc8Ei ProductLineCard_line__MqF3B"]')

    print("Всего ссылок:", len(links))
    print("-" * 60)
