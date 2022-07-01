import requests
url_endpoint = "https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={}&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-01-2021&toDate=13-10-2021&dataType=PRICEVOLUMEDELIVERABLE"
from nsetools import Nse
nse = Nse()
all_stock_codes = nse.get_stock_codes()
print("Total Stocks in NSE is {}".format(len(all_stock_codes)))
del all_stock_codes['SYMBOL']
for stock in all_stock_codes:
    if stock!='HDFCBANK':
        continue
    try:
        stock_endpoint = url_endpoint.format(stock)
        print(stock_endpoint)
        x = requests.get(stock_endpoint)
        print("{} - {}".format(stock,x.status_code))
    except Exception as e:
        print("Not able fetch details for {}".format(stock))



