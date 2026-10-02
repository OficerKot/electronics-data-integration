from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://www.mvideo.ru/catalog/audiotehnika"

driver = webdriver.Edge()

driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

print("Размер HTML:", len(html))
print("Количество ссылок:", len(soup.find_all("a")))

driver.quit()