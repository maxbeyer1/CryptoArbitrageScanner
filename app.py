from datetime import datetime
from dash import html, dcc, dash_table, dash
from dash.dependencies import Input, Output
import pandas as pd

import trades

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;400;700&display=swap',
        'rel': 'stylesheet',
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Crypto Arbitrage Scanner"

app.layout = html.Div( 
    html.Div([
        html.Div([
            html.H1("Arbitrage Scanner", className='header-title'),
            html.P("Live scanner for arbitrage opportunties across crypto exchanges -- updates every 2 minutes. All potential trades are with USDT or USD. Learn more here: ", className='header-description'),
            html.A("https://github.com/maxbeyer1/CryptoArbitrageScanner", href="https://github.com/maxbeyer1/CryptoArbitrageScanner", className='header-link'),
        ],
        className='header',
        ),
        html.Div(
            dash_table.DataTable(
                id='trades-table',
                columns=[
                    {'name': 'Coin', 'id': 'symbol'},
                    {'name': 'Profit (%)', 'id': 'profit'},
                    {'name': 'High Exchange (buy)', 'id': 'highExchange'},
                    {'name': 'Low Exchange (sell)', 'id': 'lowExchange'},
                ],

                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },

                sort_action='native'
            ),
        className='table-wrapper'
        ),
        html.Div(id='last-updated-text', className='last-updated'),
        html.Div("Powered by CoinGecko API", className="attribution-text")
        dcc.Interval(
            id = 'interval-component',
            interval = 120 * 1000, # in milliseconds --> MUST stay above 1 minute to prevent rate limiting
            n_intervals = 0
        )
    ])
)

# Update possible trades
@app.callback(
    Output(component_id='trades-table', component_property='data'),
    Input('interval-component', 'n_intervals')
)
def display_trades(n):
    coin_data = trades.get_coin_data(50)
    possible_trades = trades.get_trades(coin_data)
    df = trades.create_sorted_dataframe(possible_trades, 'profit')

    return df.to_dict('records')

# Show last updated time when updated
@app.callback(
    Output(component_id='last-updated-text', component_property='children'),
    Input('interval-component', 'n_intervals')
)
def update_text(n):
    current_time = datetime.now()
    current_time_str = current_time.strftime("%d/%m/%Y %H:%M:%S")

    return html.Span('Last updated at {ftime}.'.format(ftime = current_time_str))

if __name__ == "__main__":
    app.run_server(debug=True)