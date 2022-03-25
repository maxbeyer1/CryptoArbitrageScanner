from dash import html, dcc, dash_table, dash
from dash.dependencies import Input, Output
import pandas as pd

import trades

app = dash.Dash(__name__)

app.layout = html.Div( 
    html.Div([
        dash_table.DataTable(id='trades-table'),
        dcc.Interval(
            id = 'interval-component',
            interval = 120 * 1000, # in milliseconds
            n_intervals = 0
        )
    ])
)

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

if __name__ == "__main__":
    app.run_server(debug=True)