from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/per_price")
def get_per_price(symbol: str):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    proxies = {
        'http': 'http://proxy.server:3128',
        'https': 'http://proxy.server:3128'
    },
    response = requests.get(url)
    data = response.json()
    return {"price": data['price']}

@app.get("/list_currency")
def get_list_currency():
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    symbols = requests.get(url).json()['symbols']
    cr = [symbol['symbol'] for symbol in symbols]
    return {"currencies": cr}

@app.get("/price_for_all_crypto")
def get_price_for_all_crypto():
    lst_prices = []
    for i in get_list_currency()["currencies"]:
        lst_prices.append(get_per_price(i)["price"])
    return {"prices": lst_prices}

@app.get("/top_prices")
def get_top_prices():
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': 'BTCUSDT',  # Символ криптовалюты
        'interval': '1d',  # Интервал времени
        # 'startTime': '1679677200',  # Начало периода времени
        # 'endTime': '1681473600'  # Конец периода времени
    }
    response = requests.get(url, params=params)
    data = response.json()
    return {"data": data}
