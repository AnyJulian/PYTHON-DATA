from dash.dependencies import Input, Output
import plotly.express as px
from layouts.graphs import create_stock_graph, create_air_fresh_prediction_graph

def register_callbacks(app, df_grouped, df_stock_grouped, df_air_fresh, air_fresh_model):
    """Enregistre les callbacks pour l'application Dash."""
    @app.callback(
        Output('article-histogram', 'figure'),
        [Input('article-checklist', 'value')]
    )
    def update_histogram(selected_articles):
        filtered_df = df_grouped[df_grouped['Article'].isin(selected_articles)]
        return px.histogram(filtered_df, x='Article', y='quantit', title="Quantité par Article")
    
    @app.callback(
        Output('stock-graph', 'figure'),
        [Input('uq-checklist', 'value')]
    )
    def update_stock_graph(selected_uq):
        # Filtrer les données en fonction des unités de quantité sélectionnées
        filtered_df = df_stock_grouped[df_stock_grouped['UQ'].isin(selected_uq)]
        return create_stock_graph(filtered_df)
    
    @app.callback(
        Output('air-fresh-prediction-graph', 'figure'),
        [Input('air-fresh-slider', 'value')]
    )
    def update_air_fresh_prediction_graph(selected_value):
        # Filtrer les données en fonction de la valeur sélectionnée
        filtered_df = df_air_fresh[df_air_fresh['Air Frais'] <= selected_value]
        return create_air_fresh_prediction_graph(filtered_df, air_fresh_model)