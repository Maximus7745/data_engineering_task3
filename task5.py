import requests
from bs4 import BeautifulSoup
import json
import numpy as np

def handle_list(url):
    response = requests.get(url)
    items = list()
    soup = BeautifulSoup(response.text, 'html.parser')
    elems = soup.find_all('div', attrs={'class' : 'item-elem'})

    for elem in elems:
        item = dict()
        item['link'] = elem.find('div', attrs={'class' : 'image'}).a['href']
        item['img_url'] = elem.find('div', attrs={'class' : 'image'}).a.img['src']
        decr = elem.find('div', attrs={'class' : 'decr'})
        item['name'] = decr.strong.a.get_text().strip()
        item['order_code'] = decr.find('div', attrs={'class' : 'info'}).small.get_text().strip().replace('Код для заказа: ','')
        item['manufacturer'] = decr.find('div', attrs={'class' : 'info'}).find('span', attrs={'class' : 'text'}).get_text().strip().replace('Производитель: ','')
        item['price'] = elem.find('b', attrs={'class' : 'price-internet'}).get_text().strip()

        items.append(item)

    return items


def handle_elem(url):
    response = requests.get(url)
    item = dict()
    soup = BeautifulSoup(response.text, 'html.parser')
    block = soup.find('div', attrs={'class' : 'color-block'})
    item['name'] = block.find('span', attrs={'itemprop' : 'name'}).get_text().strip()
    item['order_code'] = block.find('span',attrs={'itemprop' : 'sku'}).get_text().strip()
    item['price'] = block.find('b',attrs={'class' : 'c1 price-internet'}).get_text().strip()
    charackters = soup.find('div', attrs={'class' : 'section-data parametrs flex'}).find_all('span')
    for span in charackters:
        item[span.u.i.get_text().strip()] = span.b.get_text().strip()

    return item

items1 = list()

for i in range(1, 18):
    url = 'https://www.avtoall.ru/zapchasti_vaz_1117_19_2192_94_kalina/?page='
    items1 += handle_list(url + f'{i}')



items2 = list()

for item in items1[ : 50]:
    url = 'https://www.avtoall.ru'
    items2.append(handle_elem(url + item['link']))

items = sorted(items1, key=lambda x: int(x['price'].replace(' ','').replace('₽','').strip()), reverse=True)


filt_items = list()
for item in items:
    if(item['manufacturer'].strip() == 'GATES'):
        filt_items.append(item)

with open('result_filt_5.json', 'w', encoding='utf-8') as f:
    json.dump(filt_items, f, ensure_ascii=False)

with open('result_all_5.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False) #Данные записывались уже отсортированными

with open('result_all_5_2.json', 'w', encoding='utf-8') as f:
    json.dump(items2, f, ensure_ascii=False)

reviews = list()

for item in items:
    reviews.append(int(item['order_code']))

result_num = {}

result_num['max'] = str(np.max(reviews))
result_num['min'] = str(np.min(reviews))
result_num['avg'] = str(np.average(reviews))
result_num['sum'] = str(np.sum(reviews))
result_num['std'] = str(np.std(reviews))

result_text = {}

for item in items:
    elem = item.get('manufacturer')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1

result_num['text'] = result_text
with open('result_5.json', 'w', encoding='utf-8') as f:
    json.dump(result_num, f, ensure_ascii=False)
