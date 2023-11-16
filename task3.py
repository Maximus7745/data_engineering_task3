from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()

    site = BeautifulSoup(text, 'xml').star
    item = dict()

    for content in site.contents:
        if(content.name is not None):
            item[content.name] = content.get_text().strip()

    return item



items = []
for i in range(1, 501):
    file_name = f"zip_var_24_3/{i}.xml"
    items.append(handle_file(file_name=file_name))





items = sorted(items, key=lambda x: float(x['distance'].replace(' million km', '').strip()), reverse=True)


filt_items = list()
for item in items:
    if(float(item['rotation'].replace(' days', '').strip()) > 365):
        filt_items.append(item)

with open('result_filt_3.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items))

with open('result_all_3.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items)) #Данные записывались уже отсортированными

radiuses = list()

for item in items:
    radiuses.append(int(item['radius']))

result_num = {}

result_num['max'] = str(np.max(radiuses))
result_num['min'] = str(np.min(radiuses))
result_num['avg'] = str(np.average(radiuses))
result_num['sum'] = str(np.sum(radiuses))
result_num['std'] = str(np.std(radiuses))

result_text = {}

for item in items:
    elem = item.get('constellation')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1

result_num['text'] = result_text
with open('result_3.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result_num))