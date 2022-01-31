from flask import app,Flask
from flask_restful import Resource, Api, reqparse
from elasticsearch import Elasticsearch
import os
import sys

INDEX_NAME = os.environ['INDEX_NAME']

app = Flask(__name__)
api = Api(app)

#Running ElasticSearch
es = Elasticsearch([{'host': 'es0', 'port': 9200}])
if es.ping():
    print('Connected to ES!')
else:
    print('Could not connect to ES!')
    sys.exit()

class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        print(self.query)
        
        #Passing the query into the pre-defined analyzer

        self.baseQuery={           
                
            "query": {
                "match": {
                    "question": {"query": "{}".format(self.query), "analyzer": "standard"}
                }
            }
        }
        

    def get(self):
        #Relevant autocomplete results for the query
        res = es.search(index=INDEX_NAME,body=self.baseQuery)
        for x in res['hits']['hits']:
            question = x['_source']['question_html']
            print(question)
        return res

parser = reqparse.RequestParser()

parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=4040)