from parsers.rbt.config import IMAGE_SELECTOR

BASE_URL = "https://www.regard.ru"

CATEGORY_URLS = {
    "smartphones": "https://www.regard.ru/catalog/1252/mobilnye-telefony",
    "tablets": "https://www.regard.ru/catalog/1264/planshety",
    "laptops": "https://www.regard.ru/catalog/1127/noutbuki",
    "computers": "https://www.regard.ru/catalog/1218/nastolnye-kompyutery",
    "monitors": "https://www.regard.ru/catalog/1035/monitory",
    "smart-watches": "https://www.regard.ru/catalog/1336/smart-casy-i-fitnes-braslety",
    "tvs": "https://www.regard.ru/catalog/1224/televizory"
}

MAX_PAGES = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

CARD_SELECTOR = "div.ListingRenderer_listingCard__s5ZKu"
VARIANT_SELECTOR = "li.SimilarGood_wrap__8IgYa"
IMAGE_SELECTOR = "img"

JSON_NAME = "regard_products.json"

REQUEST_PAUSE_TIME = 1