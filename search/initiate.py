from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import os
import sys
from build import build_document
from ingest import generate_actions
from fields import html_fields,analyzed_fields,keyword_fields,dense_vector
 

INDEX_NAME = os.environ['INDEX_NAME']

#Connecting to elasticsearch
es = Elasticsearch([{'host': 'es0', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

document = build_document(html_fields,analyzed_fields,keyword_fields,dense_vector)

#Creating an index using the above defined mapping
res = es.indices.create(index=INDEX_NAME, ignore=400,body=document)

#feeding seed data if index was just created
if 'acknowledged' in res and res['acknowledged'] == True:
    print("Ingesting seed data: ")
    for ok, response in streaming_bulk(client=es, index=INDEX_NAME, actions=generate_actions()):
        if not ok:
            print(response)
    print("Seed data ingested")