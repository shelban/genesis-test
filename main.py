from fastapi import FastAPI
import requests

app = FastAPI()


def get_current_btc_to_uah_exchange_rate():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=uah"
    response = requests.get(url)
    data = response.json()
    return data[0]['current_price']


@app.get("/rate")
def get_rate() -> int:
    return get_current_btc_to_uah_exchange_rate() 



