
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
    "tvs": "https://www.rbt.ru/cat/tele-video-audio/televizory/",
    "usb-flash-drives": "https://www.rbt.ru/cat/komputery_i_orgtehnika/usb-fleshki/",
    "routers": "https://www.rbt.ru/cat/komputery_i_orgtehnika/routery_i_setevoe_oborudovanie/",
    "computer-speakers": "https://www.rbt.ru/cat/komputery_i_orgtehnika/kompyuternye_kolonki/",
    "laser-printers": "https://www.rbt.ru/cat/komputery_i_orgtehnika/lazernye_printery/",
    "inkjet-mfu": "https://www.rbt.ru/cat/komputery_i_orgtehnika/struynye_mfu/",
    "laser-mfu": "https://www.rbt.ru/cat/komputery_i_orgtehnika/lazernye_mfu/",
    "computer-cables": "https://www.rbt.ru/cat/komputery_i_orgtehnika/kabeli_perehodniki/",
    "phone-cases": "https://www.rbt.ru/cat/cifrovye_ustroistva/chehly_dlya_smartfonov/",
    "screen-protectors": "https://www.rbt.ru/cat/cifrovye_ustroistva/plenki_i_stekla_dlya_telefonov/",
    "memory-cards": "https://www.rbt.ru/cat/cifrovye_ustroistva/karty_pamyati_microsdhc/",
    "dvb-receivers": "https://www.rbt.ru/cat/tele-video-audio/dvb-t2_resivery/",
    "soundbars": "https://www.rbt.ru/cat/tele-video-audio/saundbary/",
    "synthesizers": "https://www.rbt.ru/cat/tele-video-audio/sintezatory_i_cifrovye_fortepiano/",
    "joysticks": "https://www.rbt.ru/cat/komputery_i_orgtehnika/dzhoystiki/",
    "portable-speakers": "https://www.rbt.ru/cat/gadzhety/portativnaya_akustika/",
    "smart-speakers": "https://www.rbt.ru/cat/gadzhety/umnye_kolonki/",
    "microphones": "https://www.rbt.ru/cat/komputery_i_orgtehnika/mikrofony/",
    "webcams": "https://www.rbt.ru/cat/komputery_i_orgtehnika/veb-kamery/",
    "phone-holders": "https://www.rbt.ru/cat/cifrovye_ustroistva/derzhateli_dlya_telefonov/",
    "smart-tv-boxes": "https://www.rbt.ru/cat/tele-video-audio/smart_pristavki/",
    "laptop-stands": "https://www.rbt.ru/cat/komputery_i_orgtehnika/podstavki_dlya_noutbukov/",
}

MAX_PAGES = 1

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

JSON_NAME = "rbt_products.json"

EMPTY_MSG_SELECTOR = ".Products_emptyProducts__6oaB6"
CATALOG_SELECTOR = ".Products_mainrow__LzwOZ"
NAME_SELECTOR = ".ProductLineCard_name__GYAB3"
CARD_SELECTOR = 'div[data-testid="product-card"][data-item-id]'
PRICE_SELECTOR = ".ProductLineCard_price__ekAOe"
CHARACTERISTICS_SELECTOR = ".ProductLineCard_params__7B_bi"
IMAGE_SELECTOR = "img"