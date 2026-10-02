import requests

url = "https://www.citilink.ru"

response = requests.get(url)

print(response.text)