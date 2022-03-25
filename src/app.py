from datetime import datetime
from dash import html, dcc, dash_table, dash
from dash.dependencies import Input, Output
import pandas as pd

import trades

app = dash.Dash(__name__)

app.layout = html.Div( 
    html.Div([
        dash_table.DataTable(
            id='trades-table',
            columns=[
                {'name': 'Coin', 'id': 'symbol'},
                {'name': 'Profit (%)', 'id': 'profit'},
                {'name': 'High Exchange (buy)', 'id': 'highExchange'},
                {'name': 'Low Exchange (sell)', 'id': 'lowExchange'},
            ],
            sort_action='native'
        ),
        html.Div(id='last-updated-text'),
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

    print (df.to_dict('records'))

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