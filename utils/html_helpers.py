from urllib.parse import urljoin


def get_text(parent, selector):
    """Получает текст вложенного элемента по CSS-селектору."""

    element = parent.select_one(selector)

    if element is None:
        return None

    return element.get_text(" ", strip=True).replace("\xa0", " ")


def get_url(parent, selector, base_url):
    """Получает ссылку и преобразует её в абсолютный URL."""

    element = parent.select_one(selector)

    if element is None:
        return None

    href = element.get("href")

    if not href:
        return None

    return urljoin(base_url, href)

