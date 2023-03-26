import json
import requests

fmp_base_url_v3 = "https://financialmodelingprep.com/api/v3"
fmp_base_url_v4 = "https://financialmodelingprep.com/api/v4"

with open('fundamentals-keys.json') as f:
    fmp_key = json.loads(f.read())['fmp_key']


def get_financials(symbol, idx=0):
    j = requests.get(f"{fmp_base_url_v3}/income-statement/{symbol}?limit={idx+1}&apikey={fmp_key}").json()
    try:
        return j[idx]
    except:
        print(j)
        return {}
# get_quarterly('AAPL', 4)

def get_key_metrics(symbol):
    # https://financialmodelingprep.com/api/v3/key-metrics-ttm/AAPL?limit=40&apikey=db39ae5b594e7fde421d83fdde927c21
    return requests.get(f"{fmp_base_url_v3}/key-metrics-ttm/{symbol}?limit=1&apikey={fmp_key}").json()
# get_key_metrics('AAPL')

def get_cpi(last_n=12):
    try:
    # https://financialmodelingprep.com/api/v4/economic?name=CPI&apikey=db39ae5b594e7fde421d83fdde927c21
        return requests.get(f"{fmp_base_url_v4}/economic?name=CPI&apikey={fmp_key}").json()[:last_n]
    except:
        return []
# get_cpi()

def get_simple_stock_changes(symbol):
    # https://financialmodelingprep.com/api/v3/stock-price-change/AAPL?apikey=db39ae5b594e7fde421d83fdde927c21
        return requests.get(f"{fmp_base_url_v3}/stock-price-change/{symbol}?limit=1&apikey={fmp_key}").json()
# get_simple_stock_changes('AAPL')

def get_snapshot(symbol):
    return stock_client.get_stock_snapshot(request_params)