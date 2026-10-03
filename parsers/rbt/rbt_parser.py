import requests
from bs4 import BeautifulSoup
from config import CATEGORY_URLS


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

links_arr = list()

for category, default_url in CATEGORY_URLS.items():
	print("\n" + "=" * 60)
	print(f"КАТЕГОРИЯ: {category}")

	for page in range(8,10):
		url = f"{default_url}?=page={page}"
		print(f"URL: {url}")

		response = requests.get(
			url,
			headers=HEADERS,
			timeout=15
		)

		soup = BeautifulSoup(response.content, "html.parser")

		links = soup.select('div[class = "ProductLineCard_container__sc8Ei ProductLineCard_line__MqF3B"]')
		if(len(links) == 0):
			break
		links_arr.extend(links)

print(len(links_arr))
