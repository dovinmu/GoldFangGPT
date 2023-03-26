from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
import alpaca_trade_api as tradeapi

from collections import defaultdict
import requests
import json

BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
with open('alpaca-keys.json') as f:
    alpaca = json.loads(f.read())

stock_client = StockHistoricalDataClient(alpaca['key'], alpaca['secret'])
request_params = StockLatestQuoteRequest(symbol_or_symbols="AAPL")
api = tradeapi.REST(key_id=alpaca['key'], secret_key=alpaca['secret'], base_url=BASE_URL) # For real trading, don't enter a base_url

def trade(symbol, side, amount):
    import alpaca_trade_api as tradeapi
    BASE_URL = 'https://paper-api.alpaca.markets' # This is the base URL for paper trading
    api = tradeapi.REST(key_id=alpaca['key'], secret_key=alpaca['secret'], base_url=BASE_URL)
    api.submit_order(
      symbol=symbol, # Replace with the ticker of the stock you want to buy
      qty=amount,
      side=side,
      type='market', 
      time_in_force='gtc' # Good 'til cancelled
    )
    print("alpaca api called:", symbol, side, amount)
    
def get_asset(symbol):
    return api.get_asset(symbol)

def get_quote(symbol):
    quote = api.get_quotes(symbol, limit=1)
    return quote[0].bp

def summarize_news_list(news_list, include_body=False):
    if include_body:
        raise Exception("currently not sure how to get the body without scraping it")
    news_str = ""
    for item in news_list:
        news_str += f"{item['created_at']}: {item['headline']}"
        if len(item['summary'].strip()) > 0:
            news_str += ' – summary: '+item['summary'].replace('\n', ' ').strip() + '\n'
        else:
            news_str += '\n'
    return news_str

def get_news_dict(limit=50, symbols=[]):
    headers = {
        'Apca-Api-Key-Id': alpaca['key'],
        'Apca-Api-Secret-Key': alpaca['secret']
    }
    if len(symbols) == 0:
        j = requests.get(f'https://data.alpaca.markets/v1beta1/news?limit={limit}', headers=headers).json()
    else:
        j = requests.get(f'https://data.alpaca.markets/v1beta1/news?limit={limit}&symbols={",".join(symbols)}', headers=headers).json()
    sym_to_news = defaultdict(list)
    for item in j['news']:
        for symbol in item['symbols']:
            sym_to_news[symbol].append(item)
    return sym_to_news

    
def get_news_summary(symbol="", limit=10):
    headers = {
        'Apca-Api-Key-Id': alpaca['key'],
        'Apca-Api-Secret-Key': alpaca['secret']
    }
    if len(symbol) > 0:
        j = requests.get(f'https://data.alpaca.markets/v1beta1/news?symbols={symbol}', headers=headers).json()
    else:
        j = requests.get(f'https://data.alpaca.markets/v1beta1/news', headers=headers).json()
    news_str = ""
    for item in j['news'][:limit]:
        news_str += f"{item['created_at']}: {item['headline']}"
        if len(item['summary'].strip()) > 0:
            news_str += ' – summary: '+item['summary'].replace('\n', ' ').strip() + '\n'
        else:
            news_str += '\n'
    return news_str

def get_portfolio(init_to_zero=[]):
    portfolio = {}
    total_value = 0
    
    for symbol in init_to_zero:
        portfolio[symbol] = { 'held': 0 }
    for pos in api.list_positions():
        symbol = pos.symbol
        qty = int(pos.qty)
        portfolio[symbol] = { 'held': qty }    
        total_value += float(pos.market_value)
    acct = api.get_account()
    portfolio['cash'] = float(acct.cash)
    total_value += float(acct.cash)
    portfolio['value'] = round(total_value, 3)
    return portfolio


def get_snapshot(symbol, raise_exception=True):
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
    try:
        return stock_client.get_stock_snapshot(request_params)
    except Exception as e:
        if raise_exception:
            raise Exception(e)
        return {}


