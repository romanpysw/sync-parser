import requests
import time
import csv
from bs4 import BeautifulSoup as BS

""" Must be send to script """
""" 1. List of URLs """
""" 2. List of field .csv names """
""" 3. Name of list > element """
""" 4. List of field css names """

urls = ["https://apteka.ru/sym/leka/kost/?page=",
        "https://apteka.ru/sym/leka/gorm/?page=",
        "https://apteka.ru/sym/leka/moche/?page=",
        "https://apteka.ru/sym/leka/proti/?page=",
        "https://apteka.ru/sym/leka/derm/?page=",
        "https://apteka.ru/sym/leka/nerv/?page=",
        "https://apteka.ru/sym/leka/protiv/?page=",
        "https://apteka.ru/sym/leka/diha/?page=",
        "https://apteka.ru/sym/leka/pishe/?page=",
        "https://apteka.ru/sym/leka/proch/?page=",
        "https://apteka.ru/sym/leka/prep/?page=",
        "https://apteka.ru/sym/leka/krov/?page=",
        "https://apteka.ru/sym/leka/serd/?page=",
        "https://apteka.ru/sym/leka/prot/?page="
        ]

names = ["Товар", "Цена", "Производитель", "Ссылка"]
list_name = ".cards-list > .catalog-card"
selectors = [".catalog-card__name", ".moneyprice__roubles", ".catalog-card__vendor", "url"]

def scrap_data(url_list, names_csv, web_list_name, web_selectors):
    if not (len(names_csv) == len(web_selectors)):
        return "[ERR] can't match names and selectors!"

    wFile = open("sync-res.csv", mode = "a", encoding = 'utf-8')
    file_writer = csv.DictWriter(wFile, delimiter = ';', lineterminator = '\n', fieldnames = names_csv)
    meta_field = dict.fromkeys(names_csv)
    cur_url = 0
    count_page = 0

    while(1):
        if cur_url < len(urls):
            count_page += 1
            r = requests.get(urls[cur_url] + str(count_page))
            html = BS(r.content, 'html.parser')
            item_list = html.select(web_list_name)
            print("----------" + str(count_page) + "----------")
        else:
            break

        if len(item_list):
            for item in item_list:
                i = 0
                for cur_selector in web_selectors:
                    if web_selectors[i] == "url":
                        meta_data = item.find('a', href = True)
                        meta_field[names_csv[i]] = meta_data.get('href')
                        i += 1
                        continue

                    meta_data = item.select(web_selectors[i])
                    if not meta_data:
                        meta_field[names_csv[i]] = "NoData"
                    else:
                        meta_field[names_csv[i]] = meta_data[0].text
                    i += 1
                file_writer.writerow(meta_field)
                meta_field.clear()
                meta_field = dict.fromkeys(names_csv)
        elif not len(item_list):
            count_page = 0
            cur_url += 1
        else:
            break
    return "[OK] Parsing successed!"


if __name__ == "__main__":
    start_time = time.time()
    print(scrap_data(urls, names, list_name, selectors))
    print("By " + str(time.time() - start_time) + " seconds")
