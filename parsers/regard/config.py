BASE_URL = "https://www.regard.ru"

CATEGORY_URLS = {
    "smartphones": "https://www.regard.ru/catalog/1252/mobilnye-telefony",
    "tablets": "https://www.regard.ru/catalog/1264/planshety",
    "laptops": "https://www.regard.ru/catalog/1127/noutbuki",
    "smart-watches": "https://www.regard.ru/catalog/1336/smart-casy-i-fitnes-braslety",
}

MAX_PAGES = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CARD_SELECTOR = "div.ListingRenderer_listingCard__s5ZKu"
VARIANT_SELECTOR = "li.SimilarGood_wrap__8IgYa"

JSON_NAME = "regard_products.json"

REQUEST_PAUSE_TIME = 0.5