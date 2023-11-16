from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()

    clothings = BeautifulSoup(text, 'xml').find_all('clothing')
    items = list()
    for clothing in clothings:
        item = dict()
        for content in clothing.contents:
            if(content.name is not None):
                item[content.name] = content.get_text().strip()
        items.append(item)

    return items



items = []
for i in range(1, 101):
    file_name = f"zip_var_24_4/{i}.xml"
    items+= handle_file(file_name=file_name)

items = sorted(items, key=lambda x: int(x['price'].strip()), reverse=True)


filt_items = list()
for item in items:
    if(float(item['rating'].strip()) > 4):
        filt_items.append(item)

with open('result_filt_4.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items))

with open('result_all_4.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items)) #Данные записывались уже отсортированными

reviews = list()

for item in items:
    reviews.append(int(item['reviews']))

result_num = {}

result_num['max'] = str(np.max(reviews))
result_num['min'] = str(np.min(reviews))
result_num['avg'] = str(np.average(reviews))
result_num['sum'] = str(np.sum(reviews))
result_num['std'] = str(np.std(reviews))

result_text = {}

for item in items:
    elem = item.get('material')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1

result_num['text'] = result_text
with open('result_4.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result_num))

