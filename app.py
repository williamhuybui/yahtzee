import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, no_update, ALL, MATCH, callback_context as ctx
import numpy as np
import utils
# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

table_content_1 = [
    ('Ones', 'Sum of ones', 'ones'),
    ('Twos', 'Sum of twos', 'twos'),
    ('Threes', 'Sum of threes', 'threes'),
    ('Fours', 'Sum of fours', 'fours'),
    ('Fives', 'Sum of fives', 'fives'),
    ('Sixes', 'Sum of sixes', 'sixes'),
    ('Bonus', '35 points if 63+ in upper section', 'bonus')
]

table_content_2 = [
    ('Three of a kind', 'Sum of all dice', 'three_kind'),
    ('Four of a kind', 'Sum of all dice', 'four_kind'),
    ('Full House', '25 points', 'full_house'),
    ('Small Straight', '30 points', 'small_straight'),
    ('Large Straight', '40 points', 'large_straight'),
    ('Yahtzee', '50 points', 'yahtzee'),
    ('Chance', 'Sum of all dice', 'chance')
]

all_table = table_content_1 + table_content_2

default_dice = np.random.randint(1, 7, 5)
n = len(default_dice)
dice_group =  dbc.Row([
        dbc.Col(width = 1),
        *[dbc.Col(html.Button(default_dice[i], id = f"dice-{i}", n_clicks = 0 ,className = 'dice'), width=2) for i in range(len(default_dice))],
        dbc.Col(width = 1),
    ], className="dices"),  # Margin-bottom class
    
def create_table(table_content, table_id, num_players):
    res = []
    res.append(
        dbc.Row([
            dbc.Col(width=4, className = 'cell'),
            *[dbc.Col(f'Player {i+1}', width=4, className = f'cell player-{i+1}') for i in range(num_players)],
        ])
    )
    print(table_content)
    for i, content in enumerate(table_content):
        res.append(
            dbc.Row([
            dbc.Col(html.Div([html.Div(content[0], className = 'row-title'), 
                              html.Div(content[1], className = 'row-desc')], className = 'table-desc'),
                    width=4, className = 'cell'),
            *[dbc.Col(html.Button(children = -63 if content[0] == 'Bonus' else None,
                                id = content[2], 
                                disabled=(content[0] == 'Bonus'), className = 'score-btn'), width=4, 
                className = 'cell') for player_id in range(num_players)],
        ])
    )
    return html.Div(res)

# Define the layout of the app
app.layout = dbc.Container([
    html.H1("Yahtzee", className = 'title'),
    dbc.Row([
        dbc.Col(dice_group, width=8),
        dbc.Col(html.Button("Reroll (0/2 used)", id = 'reroll-btn', n_clicks = 0), width=4)
    ], className = 'dice-container'),
    create_table(table_content_1, 1, 1),
    html.Div(style = {'height': '30px'}),
    create_table(table_content_2, 2, 1)
])

#Callback function
@app.callback(
    [Output(f'dice-{i}', 'children') for i in range(n)],
    Input('reroll-btn', 'n_clicks'),
    [State(f'dice-{i}', 'n_clicks') for i in range(n)],
    [State(f'dice-{i}', 'children') for i in range(n)],
    prevent_initial_call=True
)
def reroll(n_clicks, *states):
    if n_clicks is None:
        return no_update
    n_clicks_list, values_list = states[:n], states[n:]
    return [np.random.randint(1, 7) if n % 2 == 0 else v for n, v in zip(n_clicks_list, values_list)]

@app.callback(
    [Output(f'dice-{i}', 'className') for i in range(n)],
    [Input(f'dice-{i}', 'n_clicks') for i in range(n)],
    prevent_initial_call=True
)
def change_color(*ns):
    return ['dice dice-selected' if n & (n % 2 == 1) else 'dice' for n in ns]

@app.callback(
    Output('reroll-btn', 'children'),
    Output('reroll-btn', 'disabled'),
    Input('reroll-btn', 'n_clicks')
)
def reroll_disabled(n_clicks):
    return f'Reroll ({n_clicks}/2 used)', n_clicks == 2

    
@app.callback(
    [Output(e[2], 'children') for e in all_table],
    [Input(f'dice-{i}', 'children') for i in range(n)],
)
def update_score(*dice_values):
    if not ctx.triggered_id:
        return no_update
    res = []
    for e in all_table:
        score = utils.get_score(dice_values, e[0])
        if e[0] == 'Bonus':
           score = sum(res) - 63 
        res.append(score)
    return res

# @app.callback(
#     Output({'type': 'score-btn', 'id': MATCH,'content': MATCH}, 'children'),
#     *[State(f'dice-{i}', 'children') for i in range(n)],
#     Input({'type': 'score-btn', 'id': MATCH, 'content': MATCH}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def update_score(*args):
#     if not ctx.triggered_id:
#         return no_update
#     dice_values = args[:n]
#     print(dice_values)
#     content = ctx.triggered_id.get('content')
#     score = utils.get_score(dice_values, content)
#     return score

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
