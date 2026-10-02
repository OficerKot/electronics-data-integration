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

    print("Статус:", response.status_code)
    print("Фактический URL:", response.url)

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", href=True)

    print("Всего ссылок:", len(links))
    print("-" * 60)
