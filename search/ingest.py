from elasticsearch import Elasticsearch
import os
import sys
from bert_serving.client import BertClient
import json
from bs4 import BeautifulSoup
from fields import analyzed_fields,keyword_fields,dense_vector

INDEX_NAME = os.environ['INDEX_NAME']

# Connecting to ElasticSearch
es = Elasticsearch([{'host': 'es0', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

bc = BertClient(ip='bertserving', output_fmt='list')
print("connected to bc")

INJESTION_FILE = os.environ['INJESTION_FILE']

def generate_actions():
    f = open(INJESTION_FILE)
    data = json.load(f)
    print(len(data))
    for id in range(min(100,len(data))):
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