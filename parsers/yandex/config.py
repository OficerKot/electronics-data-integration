from parsers.rbt.config import MAX_PAGES

BASE_URL = "https://market.yandex.ru"

CATEGORY_URLS = {
    "smartphones": "https://market.yandex.ru/catalog--smartfony-i-gadzhety/26893630/list?_redirectCount=1",
    "tablets": "https://market.yandex.ru/catalog--planshetnye-kompiutery/26908970/list?hid=6427100&rs=eJwzEvrEyMnBIMGgcGdxB_Nepr7tXXYANtYGVw%2C%2C",
    "laptops": "https://market.yandex.ru/catalog--noutbuki-personalnye/26895412/list?hid=91013&_redirectCount=1",
    "smart-watches": "https://market.yandex.ru/catalog--umnye-chasy-i-braslety/26893830/list?hid=10498025&_redirectCount=1",
    "computers": "https://market.yandex.ru/catalog--kompiutery-i-komplektuiushchie/26909890/list?hid=10604359&rs=eJwzsv3EaMLBKHB8XjurBLPGj0d3lTU6jrNqPPsAZNz4BySuP_jMqnG8556yRgtQfOssIGPpinvKe5me24s4AABcMhwo"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MAX_PAGES = 1

CARD_SELECTOR = 'div[data-zone-name="productSnippet"]'

ITEM_SELECTORS = {
    "name": '[data-auto="snippet-title"]',
    "price": '[data-auto="snippet-price-current"]',
    "url": 'a[data-auto="snippet-link"]',
    "characteristics": '._2JqZs',
    "characteristic": '.B_ssj',
    "image": 'img'
}