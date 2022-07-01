from nsetools import Nse
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from elasticsearch import Elasticsearch
from time import gmtime, strftime
nse = Nse()
all_stock_codes = nse.get_stock_codes(cached=False)
date = strftime("%Y-%m-%d", gmtime())
for stock in all_stock_codes.keys():
    hosts = "http://localhost:9200"
    es = Elasticsearch(hosts=hosts)
    if stock=='SYMBOL':
        continue
    try:
        stock_data = nse.get_quote(stock)
        id = 'nse-{}-{}'.format(stock,date)
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        stock_data['ingestionDate'] = timestamp
        stock_data['pChange'] = float(stock_data['pChange'])
        del stock_data['priceBand']
        es_response = es.index(index="stock", doc_type="nse", id=id, body=stock_data)
        print(es_response)
    except Exception as e:
        print("No information is available for {}".format(stock))
        continue