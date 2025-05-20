import psycopg2
import pandas as pd

## Voir les série temporelles de la base de données
## Streamlit : https://streamlit.io/
## Dash : https://dash.plotly.com/
## ANOVA
## 

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

# Fermer la connexion à la base de données
conn.commit()
conn.close()

# Nettoyer la colonne 'quantit' (supprimer espaces, remplacer virgules par points)
df['quantit'] = df['quantit'].astype(str).str.replace(r'[^\d.]', '', regex=True)
df['quantit'] = pd.to_numeric(df['quantit'], errors='coerce')

# Calculer la somme totale de 'quantit' pour chaque article
df_grouped = df.groupby("Article", as_index=False).sum()

# Afficher le tableau des données groupées
print(df_grouped)

# Calculer la somme totale de toutes les quantités
total_quantit = df_grouped['quantit'].sum()

print(f"Valeur totale de 'quantit' : {total_quantit}")

