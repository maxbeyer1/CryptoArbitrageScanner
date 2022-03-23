import json
from time import sleep
from pycoingecko import CoinGeckoAPI
import pandas as pd

cg = CoinGeckoAPI()

# calculate percent difference
def get_change(a, b):
    if a == b:
        return 0
    try:
        return (abs(a - b) / b) * 100.0
    except ZeroDivisionError:
        return float('inf')

# calculate profit from given ticker data (cg.get_coin_ticker_by_id)
def get_profit(coin_data):
    tickers = coin_data['tickers']

    prices = {}

    # sort through all exchanges (with high trust scores) and add to dictionary 
    for exchange in tickers:
        if (exchange['target'] == 'USDT' or exchange['target'] == 'USD') and exchange['trust_score'] == 'green':
            prices[str(exchange['market']['name'])] = exchange['last']
    
    # calculate hgihest and lowest from dictionary
    high = max(prices, key=prices.get, default=0)
    low = min(prices, key=prices.get, default=0)
    
    # calculate profit from potential trade
    if (high == 0 or low == 0):
        profit = 0
    else:
        profit = get_change(prices[low], prices[high])

    return profit, high, low

coin_tickers = {}

# get list of top 100 coins by market cap
coin_list = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc')

# add first 50 to dictionary (limited by CoinGecko API rate limits)
for coin in coin_list[:50]:
    id = coin['id']
    coin_tickers[id] = cg.get_coin_ticker_by_id(id=id)

possibleTrades = {}

# get most profitable trade for each coin
for ticker in coin_tickers:
    profit, highExchange, lowExchange = get_profit(coin_tickers[ticker])

    possibleTrades[ticker] = {
        'profit': profit,
        'highExchange': highExchange,
        'lowExchange': lowExchange
    }

max_profit_ticker = ''
max_profit = 0
max_profit_highExchange = ''
max_profit_lowExchange = ''

# find most profitable trade
for trade in possibleTrades:
    if possibleTrades[trade]['profit'] > max_profit and trade != 'tether':
        highExchange = possibleTrades[trade]['highExchange']
        lowExchange = possibleTrades[trade]['lowExchange']

        max_profit = possibleTrades[trade]['profit']
        max_profit_ticker = trade
        max_profit_highExchange = highExchange
        max_profit_lowExchange = lowExchange

# tether is not a viable arbitrage opportunity but often shows up as one due to mispricing
del possibleTrades['tether']

print ("highest profit trade is with: " + max_profit_ticker + " for a profit of " + str(max_profit))
print ("buy " + max_profit_ticker + " on " + max_profit_lowExchange + " and sell on " + max_profit_highExchange)

df = pd.DataFrame(possibleTrades).T
df.fillna(0, inplace=True)
df.sort_values(by='profit', ascending=False, inplace=True)
print(df)