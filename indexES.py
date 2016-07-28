import os, re, json, sys
import requests
from elasticsearch import Elasticsearch
import urllib3
import certifi

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

# ESURL = "https://ash-7350897.us-east-1.bonsai.io/"
# BONSAI_URL = "https://62h1ir78:aige8zcmnu1btc9l@ash-7350897.us-east-1.bonsai.io"
# bonsai = os.environ.get('BONSAI_URL', BONSAI_URL)
# auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
# host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

ES_HOST = "search-ppsandbox-6atza6pvphfjp73xqg7yhyl5qi.us-east-1.es.amazonaws.com"
#ES_HOST = "192.168.99.100"
# ES_HOST = "cf2955495bf11a3e4c0a4447f0629b84.us-east-1.aws.found.io"
#ES_HOST = "localhost"

ES_PORT=443
#ES_PORT=9200
#ES_PORT=32771
ES_HTTPS = True

#ES_HOST="localhost"
# ES_PORT=32769

# # Connect to cluster over SSL using auth for best security:
# es_header = [{
#   'host': host,
#   'port': 443,
#   'use_ssl': True,
#   'http_auth': (auth[0],auth[1])
# }]

if ES_HTTPS:
    ES_URL = "https://" + ES_HOST+":"+str(ES_PORT)
else:
    ES_URL = "http://" + ES_HOST+":"+str(ES_PORT)

# ES_PORT=9243

es_header = [{
  'host': ES_HOST,
  'port': ES_PORT,
  'use_ssl': ES_HTTPS
  # 'http_auth': (auth[0],auth[1])
}]

# DELETE EVERYTHING
print requests.delete(ES_URL+'/pp').text
# sys.exit(0)

print (ES_URL)

print "posting stuff to pp index"
# # Instantiate the new Elasticsearch connection:
es = Elasticsearch(es_header, verify_certs=False)
r = requests.post(ES_URL+"/pp", data=json.dumps({
  "mappings": {
    "method": {
      "properties": {
        "Maximum_Participants" : {
          "type": "string"
        },
        "Minimum_Participants" : {
          "type": "string"
        }
      }
    },
    "case": {
      "properties": {
        "Country" : {
          "type": "string",
          "index": "not_analyzed"
        },
        "CaseID": {
            "type":     "string",
            "analyzer": "english",
            "fields": {
                "raw": {
                    "type":  "string",
                    "index": "not_analyzed"
                }
            }
        }
      }
    }
  }
}))
# sys.exit(0)
# print r
# print r.text
#
# print requests.get(ES_URL+"/pp/case/_search").text
#
# sys.exit(0)


# i = 1
# while r.status_code == 200:
#     r = requests.get('http://swapi.co/api/people/'+ str(i))
#     print r.content
#     print json.loads(r.content)
#     # es.index(index="test", doc_type="thing", id=i, body={"a": 'foo'})
#     es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
#     i=i+1
#
# print(i)
print "posting cases"
cases = json.loads(open("mergedcases.json").read())
for case in cases[u'cases']:
    case['type'] = 'Case'
    es.index(index='pp', doc_type='case', id=case['NodeId'], body=case)

print "posting methods"

methods = json.loads(open("mergedmethods.json").read())
id = 1
for method in methods[u'methods']:
    try:
        method['type'] = 'Method'
        method['methodID'] = id
        id += 1
        es.index(index='pp', doc_type='method', id=id, body=method)
    except Exception, E:
        print repr(E)
        raise

print "posting organizations"

orgs = json.loads(open("mergedorgs.json").read())
for org in orgs[u'organizations']:
    org['type'] = 'Organization'
    es.index(index='pp', doc_type='organization', id=org['Title'], body=org)
