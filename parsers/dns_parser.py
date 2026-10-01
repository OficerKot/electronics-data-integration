import requests

url = "https://www.dns-shop.ru/catalog/17a8a01d16404e77/smartfony/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

print("Статус:", response.status_code)
print("Размер HTML:", len(response.text))
print(response.text[:1000])