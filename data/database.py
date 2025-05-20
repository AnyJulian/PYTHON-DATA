import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

def get_database_connection():
    """Établit une connexion à la base de données."""
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def fetch_data(query, columns):
    """Exécute une requête SQL et retourne un DataFrame."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=columns)