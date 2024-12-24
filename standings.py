import pandas as pd
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import warnings
from bs4 import BeautifulSoup, Comment
import requests
from navbar import navbar

warnings.filterwarnings('ignore')

website = 'https://fbref.com/en'
page = requests.get(website)
soup = BeautifulSoup(page.text)
competitions_url = soup.find_all('a', href="/en/comps/")[0].get('href').replace('/en', '')
competitions_page = website + competitions_url
page_competitions = requests.get(competitions_page)
soup_competitions = BeautifulSoup(page_competitions.text)

links = {}
for league_link in range(5):
    links.update({soup_competitions.find_all('table', id='comps_club')[0].find_all('tbody')[0].find_all('tr')[
                      league_link].find('th').find('a').get_text():
                      soup_competitions.find_all('table', id='comps_club')[0].find_all('tbody')[0].find_all('tr')[
                          league_link].find('th').find('a').get('href')})

league_links = [website.replace('/en', '') + link for link in list(links.values())]
league_links

for j, k in zip(links, league_links):
    links[j] = k
dropdown = list(links.keys())

cards = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div([
                    html.H5('Total Goals Scored', className='card_title'),

                    html.P(
                        {},
                        className='card_text',
                        id='goals'
                    ),
                ],
                    className='card_body')
            ],
                className='card mx-auto',
                style={'width': '18rem'}
            )
        ),

        dbc.Col(
            html.Div([
                html.Div([
                    html.H5('Total Red Cards', className='card_title'),
                    html.P(
                        {},
                        id='red_cards',
                        className='card_text'
                    )
                ], className='card_body')
            ], className='card mx-auto', style={'width': '18rem'})
        ),

        dbc.Col(
            html.Div([
                html.Div([
                    html.H5('Average Goal per Match', className='card_title'),
                    html.P(
                        {},
                        id='goals_match',
                        className='card_text'
                    )
                ], className='card_body')
            ], className='card mx-auto', style={'width': '18rem'})
        )
    ])
])

standings = html.Div([
    navbar,
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3('Select League: '),
                dcc.Dropdown(id='leagues', options=dropdown, value='Premier League',
                             style={'width': '50%', 'margin-right': '40px'}
                             )
            ], style={'display': "flex",
                      'justify-content': "center",
                      'align-items': "center"})
        ),
        dbc.Col(
            html.Div([
                html.H3('Season: '),
                dcc.Dropdown(id='seasons', options=[], style={'width': '50%', 'margin-left': '40px'}, value='2023-2024',
                             )
            ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        )
    ]),

    html.Br(),
    html.Br(),
    cards,

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            html.H3('Standings'),
            dcc.Loading(
                children=[html.Div([], id='table', style={'width': '50%', 'margin-right': '50px'})],

            )
        ]),

        dbc.Col([
            html.H3('Top Scorers '),
            dcc.Loading(
                children=[html.Div([], id='top_scorers', style={'width': '50%', 'margin-left': '50px'})],
                type='circle'
            )
        ])

    ], className="d-flex justify-content-around",
        style={'width': '90%', 'margin': '0 auto', 'justify': 'around'}),

], style={'font-family': "Montserrat"})


@callback(
    Output('seasons', 'options'),
    Input('leagues', 'value')
)
def update_seasons(league):
    page_1 = requests.get(links[league])  # select the league
    soup_1 = BeautifulSoup(page_1.text)

    # create a dictionary with a the link to each season's stats as the key and the season as the value
    seasons_dict = {}
    for k in range(len(soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr'))):
        seasons_dict.update({soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[k].find_all(
            'th')[0].find_all('a')[0].get('href'):
                                 soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[
                                     k].find_all('th')[0].find_all('a')[0].get_text()})

    return list(seasons_dict.values())


@callback(
    Output('seasons', 'value'),
    Input('seasons', 'options')
)
def update_initial_season(current_season):
    return current_season[0]


@callback(
    Output('table', 'children'),
    Output('goals', 'children'),
    Output('goals_match', 'children'),
    Input('leagues', 'value'),
    Input('seasons', 'value')
)
def update_standings_table(league, season):
    page_1 = requests.get(links[league])  # select the league
    soup_1 = BeautifulSoup(page_1.text)

    seasons_dict = {}
    for k in range(len(soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr'))):
        seasons_dict.update({soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[k].find_all(
            'th')[0].find_all('a')[0].get('href'):
                                 soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[
                                     k].find_all('th')[0].find_all('a')[0].get_text()})

    seasons_links = [website.replace('/en', '') + v for v in list(seasons_dict.keys())]

    selected_season = [i for i in list(seasons_dict.values()) if season in i]
    selected_links = [key for key, val in seasons_dict.items() if val in selected_season]
    print(selected_season, selected_links)
    selected_season_links = [website.replace('/en', '') + v for v in selected_links]
    selected_season_links
    page = requests.get(selected_season_links[0])
    soup = BeautifulSoup(page.text)
    standings_table = soup.find_all('table')[0]
    standings_table1 = standings_table.find_all('tbody')  # get the rows with the data
    standings_table2 = standings_table1[0].find_all('tr')  # get the rows with the data
    standings_table2

    headers = standings_table.find_all('thead')[0]
    headers = headers.find_all('th')
    headers_list = []
    for i in range(len(headers)):
        headers_list.append(headers[i].get_text())
    headers_list = headers_list[1:10]

    df = pd.DataFrame()
    team_list = []
    # extract the data
    for j in range(len(standings_table2)):
        team_details = []
        for i in range(9):
            team_details.append(standings_table2[j].find_all('td')[i].get_text())
        df = pd.concat([df, pd.DataFrame(team_details).T])
        team_list.append(team_details)

    df.columns = headers_list

    df.reset_index(drop=True, inplace=True)
    df_table = dbc.Table.from_dataframe(df.head(10), index=False, bordered=True, striped=True, hover=True,
                                        responsive=False)
    goals_scored = f"{df['GF'].astype(int).sum()} Goals"
    goals_per_match = f"{round(df['GF'].astype(int).sum() / (df['MP'].astype(int).sum() / 2), 2)} Goals Per Match"
    print(df['GF'].astype(int).tolist())
    return df_table, goals_scored, goals_per_match


@callback(
    Output('top_scorers', 'children'),
    Output('red_cards', 'children'),
    Input('leagues', 'value'),
    Input('seasons', 'value')
)
def update_topscorers(league, season):
    page_1 = requests.get(links[league])  # select the league
    soup_1 = BeautifulSoup(page_1.text)

    seasons_dict = {}
    for k in range(len(soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr'))):
        seasons_dict.update({soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[k].find_all(
            'th')[0].find_all('a')[0].get('href'):
                                 soup_1.find_all('table', id='seasons')[0].find_all('tbody')[0].find_all('tr')[
                                     k].find_all('th')[0].find_all('a')[0].get_text()})

    seasons_links = [website.replace('/en', '') + v for v in list(seasons_dict.keys())]

    selected_season = [i for i in list(seasons_dict.values()) if season in i]
    selected_links = [key for key, val in seasons_dict.items() if val in selected_season]
    selected_season_links = [website.replace('/en', '') + v for v in selected_links]
    selected_season_links
    page = requests.get(selected_season_links[0])
    soup = BeautifulSoup(page.text)

    leaderboard = soup.find_all('div', class_='leaderboard_wrapper')[0]
    comments = leaderboard.find_all(text=lambda text: isinstance(text, Comment))
    comments = BeautifulSoup(comments[0])
    goalscorers = comments.select('table.columns')[0]

    df_scorers = pd.DataFrame()
    for i in goalscorers.find_all('tr'):
        k = i.find_all('td')

        player_dets = []
        for j in k:
            player_dets.append(j.get_text().replace('\xa0', ' '))
        # df_scorers = df_scorers.append(pd.DataFrame(player_dets).T)
        df_scorers = pd.concat([df_scorers, pd.DataFrame(player_dets).T])

    df_scorers.columns = ['Rank', 'Player_Team', 'Goals']
    df_scorers['Player'] = df_scorers['Player_Team'].apply(lambda x: x.split('•')[0])
    df_scorers['Team'] = df_scorers['Player_Team'].apply(lambda x: x.split('•')[1])
    df_scorers.drop(columns=['Player_Team', 'Rank'], inplace=True)
    df_scorers

    red_cards = comments.find('div', id="leaders_cards_red").find('table').find_all('tr')
    rc = []
    for i in range(len(red_cards)):
        rc.append([x.get_text() for x in red_cards[i].find_all('td')])
    df_red_cards = pd.DataFrame(rc, columns=['rank', 'player', 'cards'])
    df_red_cards['player'] = df_red_cards['player'].apply(lambda x: x.split('•')[0])
    df_red_cards['team'] = df_red_cards['player'].apply(lambda x: x.split('•')[-1])
    df_red_cards.drop(columns=['rank'], inplace=True)
    df_red_cards['cards'] = df_red_cards['cards'].astype(int)
    total_red_cards = f"{df_red_cards['cards'].sum()} Red Cards"
    print(total_red_cards)

    df_top_scorers = dbc.Table.from_dataframe(df_scorers.head(10), index=False, bordered=True, responsive=True,
                                              hover=True,
                                              striped=True)
    return df_top_scorers, total_red_cards
