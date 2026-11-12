import re


def extract_brand_model(name):
    if not name:
        return None, None

    words = name.split()

    # Ищем первое английское слово — бренд
    brand_index = None

    for i, word in enumerate(words):
        word = word.strip(".,()[]{}")

        if re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", word):
            brand_index = i
            break

    if brand_index is None:
        return None, None

    brand = words[brand_index].strip(".,()[]{}")

    # Собираем модель до первого русского слова
    model_words = []

    for word in words[brand_index + 1:]:
        word = word.strip(".,()[]{}")

        if not word:
            continue

        # Если встретилась кириллица — заканчиваем
        if re.search(r"[А-Яа-яЁё]", word):
            break

        model_words.append(word)

    model = " ".join(model_words) if model_words else None

    return brand, model