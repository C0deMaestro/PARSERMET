import random
from parse_met import met_get_info
import requests,time
from bs4 import BeautifulSoup
from proxies import *
from headers import *
import webbrowser




url = 'https://23met.ru'
response = requests.get(url, proxies=proxies,headers=headers)
with open('response.html', 'w',encoding="UTF-8") as f:
    f.write(response.text)

soup = BeautifulSoup(response.text, 'lxml')



# получаем заголовок сайта
title = soup.title.string
print('Заголовок сайта:', title)

# получаем нужные ссылки на странице
link_met = soup.find('a', {'class': 'active', 'href': 'https://23met.ru/price'})
print("сыылка -",link_met)
met_get_info(link_met)


#link_nerch = soup.find('a', {'href': 'https://23met.ru/price_nerzh'})
# print(link_nerch)
#
# submenu = soup.find('ul', {'class': 'submenu_ul'})
# submenu_links = []
# if submenu:
#     submenu_links = [link.get('href') for link in submenu.find_all('a')]
# print(submenu_links)

# def get_met_info():
#     responce = requests.get(link_met.get("href"),proxies = proxies,headers = headers)
#     return responce
#
# print(get_met_info())



# delay = random.randint(1, 5)
# time.sleep(delay)