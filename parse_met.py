import webbrowser
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By

from proxies import *
from headers import *
from bs4 import BeautifulSoup
def met_get_info(link):
    response = requests.get(link.get("href"), proxies=proxies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    webbrowser.open_new_tab(response.url)
    driver = webdriver.Edge()
    driver.start_session({})
    # открыть страницу
    driver.get(link)
    # найти элемент с городами
    driver.implicitly_wait(2)#задержка
    cities = driver.find_elements(By.TAG_NAME, "div")
    for i in cities:
        if i.text == "в Москве Изменить/выбрать несколько":
            i.click()

    cities_checkboxes = driver.find_elements(By.CSS_SELECTOR,"input[type='checkbox']")

    print(cities_checkboxes)


met_get_info('https://23met.ru')
