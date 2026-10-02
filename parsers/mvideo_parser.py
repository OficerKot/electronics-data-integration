import requests

url = "https://www.mvideo.ru/"

response = requests.get(url)

with open("mvideo_responce.html", "w", encoding="utf-8") as file:
	file.write(response.text)

