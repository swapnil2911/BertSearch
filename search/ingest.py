from elasticsearch import Elasticsearch
import sys
from bert_serving.client import BertClient
import json
from bs4 import BeautifulSoup
from fields import analyzed_fields,keyword_fields,dense_vector

INDEX_NAME = 'StackOverflow'

# Connecting to ElasticSearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

bc = BertClient(ip='localhost', output_fmt='list')
print("connected to bc")

def generate_actions():
    f = open('injest.json')
    data = json.load(f)
    print(len(data))
    for id in range(len(data)):
        print(id)
        record = {}
        
        for field in analyzed_fields:
            record[field] = BeautifulSoup(data[id][field],'html.parser').get_text(" ", strip=True)
            record[field + '_html'] = data[id][field]
            record[dense_vector] = bc.encode([BeautifulSoup(data[id][field],'html.parser').get_text(" ", strip=True)])[0]

        for field in keyword_fields:
            record[field] = BeautifulSoup(data[id][field],'html.parser').get_text(" ", strip=True)
            record[field + '_html'] = data[id][field]

        yield record