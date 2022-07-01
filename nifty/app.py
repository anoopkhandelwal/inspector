from flask import Flask, render_template
from elasticsearch import Elasticsearch
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index(chartID = 'container', chart_type = 'spline', chart_height = 800):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    gte = "2020-09-28 00:00:00"
    total_traded_quantity = 400000
    hosts = "http://localhost:9200"
    es = Elasticsearch(hosts=hosts)
    query = {
	"query":{
		"bool":{
			"must":[
				{
					"range":{
						"pChange":{
							"gte":1

						}
					}
				},
				{
					"range":{
						"ingestionDate":{
							"gte":gte

						}
					}
				},
				{
					"range":{
						"lastPrice":{
							"lte":5000,
							"gte":50

						}
					}
				},
				{
					"range":{
						"totalTradedVolume":{
							"gte":total_traded_quantity

						}
					}
				}
				]
		}
	},
	"sort" :[ {"ingestionDate":{"order":"desc"}},{"pChange":{"order":"desc"}} ] ,
	"aggs":{
		"symbol":{
			"terms":{
				"field": "symbol.keyword"
			},
			"aggs":{
				"date":{
					"terms":{
						"field":"ingestionDate"
					},
					"aggs":{
						"pChange":{
							"terms":{
								"field":"pChange"
							}
						}
					}
				}
			}
		}
	},
	"size":10000

}
    aggs = es.search(index="stock", doc_type="nse",body=query)['aggregations']['symbol']
    stocks = aggs['buckets']
    series = []
    for stock in stocks:
        symbol = stock['key']
        dates = stock['date']['buckets']
        pChangeList = []
        dateList = []
        for date in dates:
            dateList.append(date['key'])
            pChanges = date['pChange']['buckets']
            for pChange in pChanges:
                pChangeList.append(pChange['key'])
        series_obj = {
            "name":symbol,
            "data":pChangeList
        }
        series.append(series_obj)
    title = {"text": ''}
    date = [gte]
    yAxis = {"title": {"text": ''}}
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, date=date, yAxis=yAxis)

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)