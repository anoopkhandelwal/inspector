from nsetools import Nse
import json
nse = Nse()
all_stock_codes = nse.get_stock_codes()
print("Total Stocks in NSE is {}".format(len(all_stock_codes)))
del all_stock_codes['SYMBOL']
for stock in all_stock_codes:
    try:
        quote_response = nse.get_quote(stock)
        print(stock,json.dumps(quote_response))
    except Exception as e:
        print("Not able fetch details for {}".format(stock))
