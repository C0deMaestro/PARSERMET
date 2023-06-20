import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import csv

#открытие файла для записи
w_file = open("data.csv","w")
names = ["Основной раздел","Подраздел","Размер"]
file_writer = csv.DictWriter(w_file, delimiter=";",
                             lineterminator="\r", fieldnames=names)
file_writer.writeheader()


#подключение
link = 'https://23met.ru'
driver = webdriver.Edge()
driver.get(link)
driver.implicitly_wait(5)

#получение основного раздела
head = driver.find_element(By.ID,"header")
main_section = driver.find_element(By.CLASS_NAME,"active").text

#выбор всех городов
choose_city = driver.find_element(By.XPATH,("//div[@class='citychooser_opener citychooser_opener-for-responsive ']"))
choose_city.click()
checkbox_all = driver.find_element(By.ID,"regionchooser-0")
checkbox_all.click()
save_btn = driver.find_element(By.CSS_SELECTOR,'.citychooser-save-btn')
save_btn.click()
time.sleep(2)

#получение всех подразделов(видов товара)
table = driver.find_element(By.CLASS_NAME, 'tabs')  # Замените 'tabs' на соответствующий класс таблицы
links = table.find_elements(By.TAG_NAME, 'a')
dct_links = {link.get_attribute("href"):link.text for link in links}
# Цикл по подразделу
for url_subsection in list(dct_links.keys())[4:]:

    print("1ый",dct_links[url_subsection])
    #получение подраздела
    subsection = dct_links[url_subsection]

    if url_subsection:
        driver.get(url_subsection)
        size_table = driver.find_element(By.CSS_SELECTOR,'.pane.current')
        links_sizes = size_table.find_elements(By.TAG_NAME, 'a')
        dct_sizes = {link.get_attribute("href"):link.text for link in links_sizes}
        print("dct",dct_sizes)
        # Цикл по размерам
        for url in list(dct_sizes.keys())[-1:]:

            if url:

                cur_names = ["Основной раздел","Подраздел","Размер"]

                # получение размера

                size_str = str(dct_sizes[url])

                driver.get(url)

                table = driver.find_element(By.ID, 'table-price')
                table_headers = [header.text for header in table.find_elements(By.TAG_NAME, 'th')]
                print("table_headers",table_headers)
                rewrite = False
                for head in table_headers:
                    if head not in names:
                        names.append(head)
                        rewrite = True

                    if head not in cur_names:
                        cur_names.append(head)
                print("names", names)
                if rewrite:
                    #перезапись заголовов файла
                    w_file.close()
                    with open("data.csv", "r") as r_file:
                        file_reader = csv.DictReader(r_file)
                        old_data = []
                        for row in file_reader:
                            print(row)
                            for name in names:
                                if name in row:
                                    old_row = {name: row.get(name)}
                                else:
                                    old_row = {name: ""}
                            old_data.append(old_row)
                    print("old_data", old_data)

                    w_file = open("data.csv","w")
                    file_writer = csv.DictWriter(w_file, delimiter=";",
                                                 lineterminator="\r", fieldnames=names)
                    file_writer.writeheader()
                    file_writer.writerows(old_data)
                    rewrite = False

                td_cost = ""
                for row in table.find_elements(By.TAG_NAME, 'tr'):
                    td_el_list = row.find_elements(By.TAG_NAME, 'td')
                    if td_el_list:
                        row_data = [main_section, subsection, size_str]
                        for cell in td_el_list:
                            class_name = cell.get_attribute("class")
                            text = cell.text

                            if "\n" in text:
                                text = cell.text.replace("\n","")

                            if class_name == "td_cost":
                                td_cost += text
                                continue

                            elif class_name == "td_cost2":
                                td_cost += ";" + text
                                row_data.append(td_cost)
                                td_cost = ""
                                continue

                            row_data.append(text)

                        print("row_data",row_data)
                        zapis = dict(zip(cur_names,row_data))
                        print("finaly",zapis)
                        file_writer.writerow(zapis)