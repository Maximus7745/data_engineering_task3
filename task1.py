from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    item = dict()

    site = BeautifulSoup(text, 'html.parser')
    item['type'] = site.find_all('div', attrs={'class' : "chess-wrapper"})[0].find_all('span')[0].get_text().split(':')[1].strip()
    item['title'] = site.find_all('h1')[0].get_text().split(':')[1].strip()
    address = re.split("Город:|Начало:", site.find('p').get_text().strip("\n").strip())
    item['city'] = address[1].strip()
    item['start_date'] = address[2].strip()
    item['count'] = site.find('span', attrs={'class' : "count"}).get_text().split(':')[1].strip()
    item['year'] = site.find('span', attrs={'class' : "year"}).get_text().split(':')[1].strip()
    item['min_rating'] = site.find('span', string=re.compile('Минимальный рейтинг для участия:')).get_text().split(':')[1].strip()
    item['img_url'] = site.find('img')['src']
    item['rating'] = site.find('span', string=re.compile('Рейтинг:')).get_text().split(':')[1].strip()
    item['views'] = site.find('span', string=re.compile('Просмотры:')).get_text().split(':')[1].strip()

    return item



items = []
for i in range(1, 1000):
    file_name = f"zip_var_24_1/{i}.html"
    items.append(handle_file(file_name=file_name))





items = sorted(items, key=lambda x: x['rating'], reverse=True)


filt_items = list()
for item in items:
    if(item['count'] != '6'):
        filt_items.append(item)

with open('result_filt_1.json', 'w', encoding='utf-8') as f:
    json.dump(filt_items, f, ensure_ascii=False)

with open('result_all_1.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False)
    #Данные записывались уже отсортированными

views = list()

for item in items:
    views.append(int(item['views']))

result_num = {}

result_num['max'] = str(np.max(views))
result_num['min'] = str(np.min(views))
result_num['avg'] = str(np.average(views))
result_num['sum'] = str(np.sum(views))
result_num['std'] = str(np.std(views))


result_text = {}

for item in items:
    elem = item['type']
    if(elem in result_text):
        result_text[elem] += 1
    else:
        result_text[elem] = 1

result_num['text'] = result_text
with open('result_1.json', 'w', encoding='utf-8') as f:
    json.dump(result_num, f, ensure_ascii=False)

