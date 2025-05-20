from dash.dependencies import Input, Output
import plotly.express as px

def register_callbacks(app, df_grouped):
    """Enregistre les callbacks pour l'application Dash."""
    @app.callback(
        Output('article-histogram', 'figure'),
        [Input('article-checklist', 'value')]
    )
    def update_histogram(selected_articles):
        filtered_df = df_grouped[df_grouped['Article'].isin(selected_articles)]
        return px.histogram(filtered_df, x='Article', y='quantit', title="Quantité par Article")