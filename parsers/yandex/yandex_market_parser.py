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
    response.encoding = "utf-8"

    print(f"Статус: {response.status_code}")
    print(f"Фактический URL: {response.url}")

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a", href=True)

    print(f"Всего ссылок найдено: {len(links)}")
    print("-" * 60)

    for link in links:
        text = link.get_text(" ", strip=True)
        href = link["href"]

        if text:
            print(f"TEXT: {text[:100]}")
            print(f"HREF: {href}")
            print("-" * 30)