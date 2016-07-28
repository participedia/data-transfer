import json
import sys
ES_BASE = "https://search-ppsandbox-6atza6pvphfjp73xqg7yhyl5qi.us-east-1.es.amazonaws.com/";
ES_INDEX = "pp";
ES_URL = ES_BASE + ES_INDEX;

ES_URL = "http://cf2955495bf11a3e4c0a4447f0629b84.us-east-1.aws.found.io:9200"


import requests

URL = ES_URL + "/pp/_search?pretty";
#
# print URL
#
# # print requests.delete(ES_URL+'/_all').text
# #
# # #
# r = requests.get(URL , data=json.dumps({
#   "size": "0",
#   "aggs": {
#     "countries": {
#       "terms": {
#         "field": "Country"
#       }
#     }
#   }
# }))
#
# print r.text
#
# sys.exit(0)




from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

import logging
logging.basicConfig()
#
# logging.getLogger("elasticsearch.trace").setLevel(logging.INFO)

client = Elasticsearch(['cf2955495bf11a3e4c0a4447f0629b84.us-east-1.aws.found.io:9200'])

s = Search(using=client, index="pp")

s.aggs.bucket('countries', 'terms', field='Country', size="0")

tracer = logging.getLogger('elasticsearch.trace')
tracer.addHandler(logging.FileHandler('elasticsearch-log.sh'))
tracer.setLevel(logging.DEBUG)


response = s.execute()

for hit in response:
    print(hit.meta.score, hit.CaseID)

for tag in response.aggregations.countries.buckets:
    print tag
    # print(tag.key, tag.Country.value)
