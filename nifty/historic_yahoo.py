import requests
import yfinance as yf
from nsetools import Nse
import pandas as pd
nse = Nse()
all_stock_codes = nse.get_stock_codes()
print("Total Stocks in NSE is {}".format(len(all_stock_codes)))
del all_stock_codes['SYMBOL']
start = '2020-03-01'
end = '2021-11-08'
stock_frame = pd.DataFrame()
for stock in all_stock_codes:
    try:
        data = []
        name='{}.NS'.format(stock)
        data = yf.download(name,start=start, end=end, progress=False)
        if len(data) == 0:
            print("Data not present for {}".format(stock))
        else:
            data['Name'] = name
            stock_frame = stock_frame.append(data, sort=False)
            print("Added {} in frame".format(stock))
    except Exception as e:
        print("Not able fetch details for {}".format(stock))

stock_frame.to_csv("historic.csv")

