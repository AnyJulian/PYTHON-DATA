from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.graphs import create_silo_graph, create_air_fresh_graph, create_stock_graph, create_blocage_graph

def create_layout(checklist_options, df_silo, df_air_fresh, df_stock, df_blocage):
    """Crée le layout principal de l'application."""
    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([html.H1("Dashboard", className="card-title")]), className="mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Label("Sélectionnez les articles à afficher :"),
                dcc.Checklist(
                    id='article-checklist',
                    options=checklist_options,
                    value=[opt['value'] for opt in checklist_options],
                    inline=True
                )
            ], width=12)
        ]),

        dbc.Row([
            dcc.Graph(id='article-histogram')  # Graphique 1
        ]),
        dbc.Row([
            dcc.Graph(figure=create_silo_graph(df_silo))  # Graphique 2
        ]),
        dbc.Row([
            dcc.Graph(figure=create_air_fresh_graph(df_air_fresh))  # Graphique 3
        ]),
                dbc.Row([
            dbc.Col([
                html.Label("Afficher les unités de quantité :"),
                dcc.Checklist(
                    id='uq-checklist',
                    options=[
                        {'label': 'SAC', 'value': 'SAC'},
                        {'label': 'TO', 'value': 'TO'}
                    ],
                    value=['SAC', 'TO'],  # Par défaut, tout est affiché
                    inline=True
                )
            ], width=12)
        ]),
        dbc.Row([
            dcc.Graph(id='stock-graph')  # Graphique 4 : Mouvements de stock (mis à jour dynamiquement)
        ]),
        dbc.Row([
            dcc.Graph(figure=create_blocage_graph(df_blocage))  # Graphique 5 : Blocages et déblocages
        ])
    ], fluid=True)