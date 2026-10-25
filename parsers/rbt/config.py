BASE_URL = "https://www.rbt.ru"

CATEGORY_URLS = {
    "smartphones": "https://www.rbt.ru/cat/cifrovye_ustroistva/smartfony/",
    "accumulators": "https://www.rbt.ru/cat/cifrovye_ustroistva/vneshnie_akkumulyatory/",
    "chargers": "https://www.rbt.ru/cat/cifrovye_ustroistva/zaryadnye_ustroystva_c277/",
    "mouses": "https://www.rbt.ru/cat/komputery_i_orgtehnika/kompyuternye_myshi/",
    "keyboards": "https://www.rbt.ru/cat/komputery_i_orgtehnika/klaviatury/",
    "tablets": "https://www.rbt.ru/cat/cifrovye_ustroistva/planshety/",
    "laptops": "https://www.rbt.ru/cat/kompyutery_i_orgtehnika/noutbuki/",
    "smart-watches": "https://www.rbt.ru/cat/gadzhety/smart_chasy/",
    "fitness-brasleti": "https://www.rbt.ru/cat/gadzhety/fitnes_braslety/",
    "headphones": "https://www.rbt.ru/cat/cifrovye_ustroistva/naushniki_i_garnitury/",
    "music_centers": "https://www.rbt.ru/cat/tele-video-audio/muzykalnye_centry/",
    "monitors": "https://www.rbt.ru/cat/komputery_i_orgtehnika/monitory/",
    "tvs": "https://www.rbt.ru/cat/tele-video-audio/televizory/"
}

MAX_PAGES = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

JSON_NAME = "rbt_products.json"

EMPTY_MSG_SELECTOR = ".Products_emptyProducts__6oaB6"
CATALOG_SELECTOR = ".Products_mainrow__LzwOZ"
ITEM_SELECTOR = ".ProductTileCard_title__Qis9q"
PRICE_SELECTOR = ".ProductTileCard_price__SnkfM"