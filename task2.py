from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    items = list()

    site = BeautifulSoup(text, 'html.parser')
    products = site.find_all('div', attrs={'class' : 'product-item'})

    for product in products:
        item = dict()
        item['id'] = product.a['data-id']
        item['link'] = product.find_all('a')[1]['href']
        item['img_url'] = product.find_all('img')[0]['src']
        item['title'] = product.find_all('span')[0].get_text().strip()
        item['price'] = int(product.price.get_text().replace('₽', '').replace(' ','').strip())
        item['bonus'] = int(product.strong.get_text().replace('+ начислим ', '').replace(' бонусов','').strip())

        props = product.ul.find_all('li')
        for prop in props:
            item[prop['type']] = prop.get_text().strip()
        items.append(item)

    return items



items = []
for i in range(1, 82):
    file_name = f"zip_var_24_2/{i}.html"
    items += (handle_file(file_name=file_name))





items = sorted(items, key=lambda x: x['id'], reverse=True)


filt_items = list()
for item in items:
    if(item['bonus'] > 700):
        filt_items.append(item)

with open('result_filt_2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items))

with open('result_all_2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items)) #Данные записывались уже отсортированными

prices = list()

for item in items:
    prices.append(int(item['price']))

result_num = {}

result_num['max'] = str(np.max(prices))
result_num['min'] = str(np.min(prices))
result_num['avg'] = str(np.average(prices))
result_num['sum'] = str(np.sum(prices))
result_num['std'] = str(np.std(prices))

result_text = {}

for item in items:
    elem = item.get('matrix')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1

result_num['text'] = result_text
with open('result_2.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result_num))