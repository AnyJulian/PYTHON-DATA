from dash import Dash
import dash_bootstrap_components as dbc
from data.database import fetch_data
from data.data_processing import process_blocage_data, process_sales_data, process_stock_data, process_time_series_data, process_sales_daily_data, process_air_fresh_data, train_air_fresh_model, add_cost_prediction
from layouts.layout import create_layout
from callbacks.callbacks import register_callbacks
from layouts.graphs import create_silo_graph, create_air_fresh_graph

# Charger les données
sales_query = "SELECT article, quantit FROM raw.ventes"
sales_columns = ["Article", "quantit"]
df_sales = fetch_data(sales_query, sales_columns)
df_grouped = process_sales_data(df_sales)

# Charger les données pour les graphiques 2 et 3
silo_query = """
    SELECT dateheure, ref_silo12_niv_t, ref_silo13_niv_t, ref_silo14_niv_t, ref_silo15_niv_t
    FROM snd_grp5.ordonnancement_broyage_clean
"""
silo_columns = ["Date", "silo12", "silo13", "silo14", "silo15"]
df_silo = fetch_data(silo_query, silo_columns)
df_silo = process_time_series_data(df_silo, date_column="Date", numeric_columns=["silo12", "silo13", "silo14", "silo15"])

air_fresh_query = """
    SELECT dateheure, ref_airfrais_temp_c
    FROM raw.prj_ord_broyage_01_2025
"""
air_fresh_columns = ["Date", "Air Frais"]
df_air_fresh = fetch_data(air_fresh_query, air_fresh_columns)
df_air_fresh = process_time_series_data(df_air_fresh, date_column="Date", numeric_columns=["Air Frais"])

# Traiter les données d'air frais
df_air_fresh = process_air_fresh_data(df_air_fresh)

# Entraîner le modèle de prédiction
air_fresh_model, X_test, y_test = train_air_fresh_model(df_air_fresh)

# Ajouter la prédiction du coût dans les données d'air frais
df_air_fresh = add_cost_prediction(df_air_fresh, air_fresh_model)

# Charger les données pour les mouvements de stock
stock_query = """
    SELECT article, mvt, quantit, uq
    FROM raw.declaration_production
"""
stock_columns = ["Article", "Mvt", "Quantit", "UQ"]

# Charger et traiter les données de stock
df_stock = fetch_data(stock_query, stock_columns)
df_stock_grouped = process_stock_data(df_stock)

# Charger les données pour les blocages et déblocages de stock
blocage_query = """
    SELECT article, mvt, quantit
    FROM raw.blocage_deblocage_stocks
"""
blocage_columns = ["Article", "Mvt", "Quantit"]

# Charger et traiter les données de blocage/déblocage
df_blocage = fetch_data(blocage_query, blocage_columns) 
df_blocage_grouped = process_blocage_data(df_blocage)

# Options pour la checklist
checklist_options = [{'label': article, 'value': article} for article in df_grouped['Article']]

# Charger les données des ventes journalières
daily_sales_query = """
    SELECT article, quantit, date_cpt
    FROM raw.ventes
"""
daily_sales_columns = ["Article", "Quantité", "Date Comptable"]
df_daily_sales = fetch_data(daily_sales_query, daily_sales_columns)

# Traiter les données des ventes journalières
df_sales_daily = process_sales_daily_data(df_daily_sales)

# Initialiser l'application
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.layout = create_layout(checklist_options, df_silo, df_air_fresh, df_stock_grouped, df_blocage_grouped, df_sales_daily)

# Enregistrer les callbacks
register_callbacks(app, df_grouped, df_stock_grouped, df_air_fresh, air_fresh_model)

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)