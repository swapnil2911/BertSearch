from elasticsearch import Elasticsearch
import os
import sys
# import pytesseract
# from PIL import Image
import requests
from flask import Flask,render_template, jsonify, request
from bert_serving.client import BertClient

INDEX_NAME = os.environ['INDEX_NAME']

# Connecting to ElasticSearch
es = Elasticsearch([{'host': 'es0', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
    bc = BertClient(ip='bertserving',output_fmt='list')
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
@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    data = request.form.get("data")
    payload = {}
    headers= {}
    url = "http://autofill:4040/autocomplete?query="+str(data)
    print(url)
    response = requests.request("GET", url, headers=headers, data = payload)
    return response.json()

if __name__ == '__main__':
    # pytesseract.pytesseract.tesseract_cmd = r'D:\Pytesseract\tesseract'
    app.run( host='0.0.0.0',debug=True,port=8080)
