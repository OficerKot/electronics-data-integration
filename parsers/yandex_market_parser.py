import requests

url = "https://market.yandex.ru"

response = requests.get(url)

print(response.text)