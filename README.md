
# Crypto Arbitrage Scanner

Proof-of-concept scanner for cryptocurrency arbitrage opportunities. Built with Python and Dash.

Scans the top 50 coins on [CoinGecko](https://www.coingecko.com/) and all available USD/USDT pairs 
to trade on every trusted exchange, and calculates the highest profit arbitrage trades to make. 

_This app or any data it presents is not financial advice. 
This is a proof-of-concept that has many flaws, so do your own research._
## Demo

See it live at: https://arbitragescanner.herokuapp.com/


## Getting Started

1. Clone the repo/download the .zip and extract to a folder

2. Install the requirements

```bash
  pip install -r requirements.txt
```
3. Start the web server

```bash
  python app.py
```

4. View the app at http://localhost:8050/
## Roadmap

- Incorporate maker/taker fees and any transfer fees into profit calculations

- Add more support for smaller coins

- Create demo trading bot based off of arbitrage data 


## License

This project is licensed under the [AGPL-3.0 License](https://choosealicense.com/licenses/agpl-3.0/).

See [LICENSE](https://github.com/maxbeyer1/CryptoArbitrageScanner/blob/main/LICENSE) for more information.

## Acknowledgements

 - https://github.com/man-c/pycoingecko
