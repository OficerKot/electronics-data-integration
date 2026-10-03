from selenium import webdriver
from bs4 import BeautifulSoup
from config import CATEGORY_URLS
import time


driver = webdriver.Edge()
for cat, url in CATEGORY_URLS.items():

	print("Категория ", cat)
	driver.get(url)

	html = driver.page_source

	soup = BeautifulSoup(html, "html.parser")
	cards = soup.select('div[class = "Card_wrap__pwcgw Card_listing__NKBPR ListingRenderer_listingCard__s5ZKu"]')
	print("Найдено карточек: ", len(cards))

	
driver.quit()

