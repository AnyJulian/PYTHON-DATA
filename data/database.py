import psycopg2
import pandas as pd

def get_database_connection():
    """Établit une connexion à la base de données."""
    return psycopg2.connect(
        database="dwh",
        user="grp5",
        host="postgresql-6dc219af-oc5eb1476.database.cloud.ovh.net",
        password="0Z8vfQqR7w3TjcA",
        port=20184
    )

def fetch_data(query, columns):
    """Exécute une requête SQL et retourne un DataFrame."""
    conn = get_database_connection()
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=columns)