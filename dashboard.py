# Import packages
from dash import Dash, html, dash_table, dcc
import dash
import pandas as pd
import plotly.express as px
import psycopg2
import dash_bootstrap_components as dbc

# Dictionnaire de correspondance entre les articles et leurs désignations
article_mapping = {
    "L10303A4121": "X Plus 25kg 45s PalEur",
    "L10300A4122": "X L 25kg 45s PalEur",
    "L10028A5320": "LUTÈCE® PROJECTION 33XPLUS 33KG 35S",
    "L10028A5113": "LUTÈCE® PROJECTION 33XPLUS 33KG 45S",
    "L10275A4121": "X Pro 25kg 45s PalEur",
    "L10309A4121": "Lutèce® Projection Excelent 25kg 45s PE",
    "L10274A5111": "LUTÈCE® PROJECTION 33XPERT 33KG 35S",
    "L10274A5110": "LUTÈCE® PROJECTION 33XPERT 33KG 45S",
    "L10301A4121": "PL Express BNL 25kg  45s palette Europe",
    "L10341A4121": "PL Classique BNL new 25kg 45s pal Europe",
    "L10340A4121": "PL Finesse NL 25kg 45s palette Europe",
    "L10319A4121": "AEROBLUE 25KGS 50S",
    "L10016A4220": "Gyproc® OneCoat plaster 25kg 50s",
    "L10014A4220": "LUTÈCE® 25 AIR PUR 50S",
    "L10013A5120": "LUTÈCE 2000® COURT 33KG 45S",
    "L10014A5120": "LUTÈCE 2000® LONG 33KG 45S",
    "L10023A5113": "LUTÈCE® PROJECTION 33X 33KG 45S",
    "L40555A5120": "LUTÈCE® FLAM 33KG 45S",
    "L10279A4120": "Royal 25kg 45s",
    "L10279A025": "Suprême 25kg 45sc",
    "A88900035P4": "MAP® 25KG  FORMULE + 35S PAL 4E",
    "A88900035": "MAP® 25KG  FORMULE + 35S",
    "A88900063": "MAP® 25KG  FORMULE + 63S",
    "A88900163": "MAP® 25kg (+10% offert)",
    "A89900056": "MORTIER ADHÉSIF JOKER® 25KG 56S",
    "A88400063": "Placo® MA24 25kg 63sc",
    "L10310A4121": "LUTÈCE® ROUGE 25KG 63S",
    "L10311A4122": "LUTÈCE® BLEU 25KG 63S",
    "L10320A4121": "FACILIS POLYVALENT 25KG 56S",
    "L10122A4122": "JOKER® SPECIAL FINITION 25KG 56S",
    "L10315A4120": "LUTÈCE® MULTIC 25KG 63S",
    "L10313A4121": "LUTÈCE® EXPRESS 25KG 63S",
    "L10321A4121": "FACILIS EXPRESS 25KG 56S",
    "L10121A4123": "JOKER® MULTI-USAGE 25KG 56S",
    "L10103A4202": "LUTÈCE® BATIBRIC® 25KG 63S",
    "L10019A4121": "PLATREX 25KG 63S",
    "L10150A4101": "LUTÈCE® GROS 25KG 63S",
    "L10275A0000": "X Pro Vrac",
    "L1030300000": "X Plus Vrac",
    "L1030000000": "XL vrac",
    "L1030400000": "Lutèce® Gros Vrac",
    "L1006000000": "Plâtre Surcuit Vrac"
}

# Initialize the app - incorporate a Dash Bootstrap theme
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Incorporate data
# Connexion à la base de données
conn = psycopg2.connect(database="dwh", 
                        user="grp5", 
                        host='postgresql-6dc219af-oc5eb1476.database.cloud.ovh.net',
                        password="0Z8vfQqR7w3TjcA",
                        port=20184)

cur = conn.cursor()

# Requête SQL pour récupérer les colonnes pertinentes
cur.execute('''
    SELECT article, quantit
    FROM raw.ventes
''')
rows = cur.fetchall()
columns = ["Article", "quantit"]

# Convertir les données en DataFrame pour une meilleure manipulation
df = pd.DataFrame(rows, columns=columns)

# Deuxième requête SQL
cur.execute('''
    SELECT dateheure, ref_silo12_niv_t, ref_silo13_niv_t, ref_silo14_niv_t, ref_silo15_niv_t
    FROM snd_grp5.ordonnancement_broyage_clean
''')
rows2 = cur.fetchall()
columns2 = ["Date", "silo12", "silo13", "silo14", "silo15"]

# Convertir les données en DataFrame pour une meilleure manipulation
df2 = pd.DataFrame(rows2, columns=columns2)

# Troisième requête SQL
cur.execute('''
    SELECT dateheure, ref_airfrais_temp_c
    FROM raw.prj_ord_broyage_01_2025
''')
rows3 = cur.fetchall()
columns3 = ["Date", "Air Frais"]

# Convertir les données en DataFrame pour une meilleure manipulation
df3 = pd.DataFrame(rows3, columns=columns3)

# Fermer la connexion à la base de données
conn.commit()
conn.close()

# Nettoyer la colonne 'quantit' (supprimer espaces, remplacer virgules par points)
df['quantit'] = df['quantit'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['quantit'] = pd.to_numeric(df['quantit'], errors='coerce')

# Supprimer les lignes où 'Article' est NaN
df = df.dropna(subset=['Article'])

# Calculer la somme totale de 'quantit' pour chaque article
df_grouped = df.groupby("Article", as_index=False).sum()

# Remplacer les numéros d'article par leurs désignations
df_grouped['Article'] = df_grouped['Article'].map(article_mapping)

# Remplacer les NaN par "Inconnu"
df_grouped['Article'] = df_grouped['Article'].fillna("Inconnu")

# Générer les options pour la checklist
checklist_options = [{'label': article, 'value': article} for article in df_grouped['Article']]

# Convertir la colonne 'Date' en type datetime pour df2
df2['Date'] = pd.to_datetime(df2['Date'])

# Trier df2 par date dans l'ordre croissant
df2 = df2.sort_values(by='Date')

# Convertir la colonne 'Date' en type datetime pour df3
df3['Date'] = pd.to_datetime(df3['Date'])

# Convertir la colonne 'Air Frais' en type numérique pour garantir un tri correct
df3['Air Frais'] = pd.to_numeric(df3['Air Frais'], errors='coerce')

# Trier df3 par la colonne 'Date' dans l'ordre croissant
df3 = df3.sort_values(by='Date')

# Initialize the app
app = Dash()

# Exemple de carte pour un graphique
card = dbc.Card(
    dbc.CardBody([
        html.H1("Dashbord", className="card-title"),
    ]),
    className="mb-4"
)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(card, width=12)
    ]),
    # Ajouter une checklist pour filtrer les articles
    dbc.Row([
        dbc.Col([
            html.Label("Sélectionnez les articles à afficher :"),
            # Ajouter une checklist pour filtrer les articles
            dcc.Checklist(
                id='article-checklist',
                options=checklist_options,  # Utiliser les options générées
                value=df_grouped['Article'].tolist(),  # Par défaut, tous les articles sont sélectionnés
                inline=True
            )
        ], width=12)
    ]),
    # Premier graphique : Histogramme des quantités par article
    dbc.Row([
        dcc.Graph(id='article-histogram')  # Graphique mis à jour dynamiquement
    ]),
    # Deuxième graphique : Évolution des niveaux des silos au fil du temps
    dbc.Row([
        dcc.Graph(
            figure=px.line(
                df2,
                x='Date',
                y=['silo12', 'silo13', 'silo14', 'silo15'],
                title="Évolution des niveaux des silos au fil du temps",
                labels={'value': 'Niveau', 'variable': 'Silo'}
            )
        )
    ]),
    # Troisième graphique : Évolution des niveaux d'air entrant au fil du temps
    dbc.Row([
        dcc.Graph(
            figure=px.line(
                df3,
                x='Date',
                y='Air Frais',
                title="Évolution des niveaux d'air frais rentrant au fil du temps",
                labels={'value': 'Niveau'}
            )
        )
    ])
], fluid=True)

# Callback pour mettre à jour le graphique en fonction des articles sélectionnés
@app.callback(
    dash.dependencies.Output('article-histogram', 'figure'),
    [dash.dependencies.Input('article-checklist', 'value')]
)
def update_histogram(selected_articles):
    # Filtrer les données en fonction des articles sélectionnés
    filtered_df = df_grouped[df_grouped['Article'].isin(selected_articles)]
    # Créer un histogramme mis à jour
    fig = px.histogram(filtered_df, x='Article', y='quantit', title="Quantité par Article")
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)