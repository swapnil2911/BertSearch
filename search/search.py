from elasticsearch import Elasticsearch
import os
import sys
# import pytesseract
# from PIL import Image
import requests
from flask import app,Flask,render_template, request
from bert_serving.client import BertClient

INDEX_NAME = os.environ['INDEX_NAME']

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Connecting to ElasticSearch
es = Elasticsearch([{'host': 'es0', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

bc = BertClient(ip='bertserving', output_fmt='list')
print("connected to bc")

#Home Page
@app.route('/')
def index():
    return render_template('index.html')

# #Image Search 
# @app.route('/image_search',methods=['GET'])
# def image_search():
#     return render_template('image_search.html')

#Search Results
@app.route('/return_searches', methods=['POST'])
def return_searches():
    result_sup = []
    query = request.form.to_dict()['query']

    query_vector = bc.encode([query])[0]

    search_query ={
        "query" : {
            "script_score" : {
                "query" : {
                    "multi_match" : {
                        "query": query, 
                        "fields": [ "question", "details" ] 
                    }
                },
                "script" : {
                    "source": "cosineSimilarity(params.query_vector, doc['total_vectors']) + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    }
    query = {
        "query" : {
            "multi_match" : {
                "query": query, 
                "fields": [ "question", "details","answers" ] 
            }
        }
    }

    print(search_query)

    res= es.search(index=INDEX_NAME,body=search_query)
    print(len(res['hits']['hits']))

    for x in res['hits']['hits']:
        question = x['_source']['question_html']
        details = x['_source']['details_html']
        answer = x['_source']['answers_html']
        result_sup.append([question,details,answer])
    return render_template('search.html',result=result_sup)


#Autocomplete the search query 
@app.route('/autocomplete', methods=["GET", "POST"])
def pipe():
    query = request.form.get("data")
    autofill_query = {             
        "query": {
            "match": {
                "question": {"query": "{}".format(query), "analyzer": "standard"}
            }
        }
    }
    response = es.search(index=INDEX_NAME,body=autofill_query)
    return response

# Autocomplete

if __name__ == '__main__':
    # pytesseract.pytesseract.tesseract_cmd = r'D:\Pytesseract\tesseract'
    app.run( host='0.0.0.0',debug=True,port=8080)
