from datetime import datetime


def extract_date_parsed():
    """Возвращает дату и время парсинга."""
    return datetime.now().isoformat(timespec="seconds")