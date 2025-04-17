import requests
import json
import time

# Kraken API settings
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"
api_url = "https://api.kraken.com"

# Bot settings
asset = "BTC"
fiat = "USD"
market = "spot"
position_size = 0.1
stop_loss_percent = 0.1
take_profit_percent = 0.1

# Moving Average parameters
ma_period_1 = 50
ma_period_2 = 200

# Calculate Moving Averages
def calculate_ma(prices, period):
    return sum(prices[-period:]) / period

while True:
    # Get current prices
    response = requests.get(api_url + "/public/Ticker", params={"pair": asset + fiat})
    print(response.json())
    prices = response.json()["result"][asset + fiat]["a"][0]

    # Calculate Moving Averages
    ma_1 = calculate_ma(prices, ma_period_1)
    ma_2 = calculate_ma(prices, ma_period_2)

    # Check for trend reversal
    if ma_1 > ma_2 and prices > ma_2:
        # Enter long position
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "buy", "ordertype": "limit", "price": prices, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Entered long position at", prices)

        # Set Take-Profit Order
        take_profit_price = prices * (1 + take_profit_percent / 100)
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "sell", "ordertype": "limit", "price": take_profit_price, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Set Take-Profit Order at", take_profit_price)

        # Set Stop-Loss Order
        stop_loss_price = prices * (1 - stop_loss_percent / 100)
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "sell", "ordertype": "stop-loss", "price": stop_loss_price, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Set Stop-Loss Order at", stop_loss_price)

    elif ma_1 < ma_2 and prices < ma_2:
        # Enter short position
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "sell", "ordertype": "limit", "price": prices, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Entered short position at", prices)

        # Set Take-Profit Order
        take_profit_price = prices * (1 - take_profit_percent / 100)
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "buy", "ordertype": "limit", "price": take_profit_price, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Set Take-Profit Order at", take_profit_price)

        # Set Stop-Loss Order
        stop_loss_price = prices * (1 + stop_loss_percent / 100)
        response = requests.post(api_url + "/private/AddOrder", data={"pair": asset + fiat, "type": "buy", "ordertype": "stop-loss", "price": stop_loss_price, "volume": position_size}, headers={"API-Key": api_key, "API-Sign": api_secret})
        print("Set Stop-Loss Order at", stop_loss_price)

    time.sleep(60)  # Wait 1 minute before checking again
