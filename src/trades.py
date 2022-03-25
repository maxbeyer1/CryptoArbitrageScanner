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
        if (
            (exchange['target'] == 'USDT' or exchange['target'] == 'USD') and
             exchange['trust_score'] == 'green' and
             exchange['market']['name'] != 'eToroX' # does not allow withdraw of crypto
        ):
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

# returns array of top coins from CoinGecko
def get_coin_data(numCoins):
    coin_tickers = {}

    # get list of top 100 coins by market cap
    coin_list = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc')

    # add first 50 to dictionary (limited by CoinGecko API rate limits)
    for coin in coin_list[:numCoins]:
        id = coin['id']
        coin_tickers[id] = cg.get_coin_ticker_by_id(id=id)
    
    return coin_tickers

def get_trades(coin_data):
    possible_trades = {}

    # get most profitable trade for each coin
    for ticker in coin_data:
        profit, highExchange, lowExchange = get_profit(coin_data[ticker])

        possible_trades[ticker] = {
            'symbol': ticker,
            'profit': profit,
            'highExchange': highExchange,
            'lowExchange': lowExchange
        }
    
    # tether is not a viable arbitrage opportunity but often shows up as one due to mispricing
    del possible_trades['tether']

    return possible_trades

# finds highest profit trade from possible trades
def suggest_trade(possible_trades):
    max_profit_ticker = ''
    max_profit = 0
    max_profit_highExchange = ''
    max_profit_lowExchange = ''

    # find most profitable trade
    for trade in possible_trades:
        if possible_trades[trade]['profit'] > max_profit:

            highExchange = possible_trades[trade]['highExchange']
            lowExchange = possible_trades[trade]['lowExchange']

            max_profit = possible_trades[trade]['profit']
            max_profit_ticker = trade
            max_profit_highExchange = highExchange
            max_profit_lowExchange = lowExchange

    print ("highest profit trade is with: " + max_profit_ticker + " for a profit of " + str(max_profit))
    print ("buy " + max_profit_ticker + " on " + max_profit_lowExchange + " and sell on " + max_profit_highExchange)

# create and sort dataframe with key from dict
def create_sorted_dataframe(data, sort_key):
    df = pd.DataFrame(data).T
    df.fillna(0, inplace=True)
    df.sort_values(by=sort_key, ascending=False, inplace=True)  

    return df

# coin_data = get_coin_data(50)
# possible_trades = get_trades(coin_data)
# suggest_trade(possible_trades)

# sorted_trades_df = create_sorted_dataframe(possible_trades, 'profit')

# print(sorted_trades_df)