import pandas as pd
from utils.constants import article_mapping

def process_sales_data(df):
    """Nettoie et transforme les données de ventes."""
    df['quantit'] = df['quantit'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['quantit'] = pd.to_numeric(df['quantit'], errors='coerce')
    df = df.dropna(subset=['Article'])
    df_grouped = df.groupby("Article", as_index=False).sum()
    df_grouped['Article'] = df_grouped['Article'].map(article_mapping).fillna("Inconnu")
    return df_grouped

def process_time_series_data(df, date_column, numeric_columns):
    """Nettoie et trie les données temporelles."""
    df[date_column] = pd.to_datetime(df[date_column])
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df.sort_values(by=date_column)

def process_stock_data(df):
    """Traite les données de stock pour séparer les entrées et sorties par article."""
    # Convertir les colonnes en types appropriés
    df['Quantit'] = pd.to_numeric(df['Quantit'], errors='coerce')
    df['Mvt'] = pd.to_numeric(df['Mvt'], errors='coerce')

    # Filtrer les lignes valides
    df = df.dropna(subset=['Article', 'Mvt', 'Quantit', 'UQ']).copy()

    # Remplacer les numéros d'article par leurs noms
    df['Article'] = df['Article'].map(article_mapping).fillna("Inconnu")

    # Créer des colonnes pour les entrées et sorties
    df['Entrée'] = df.apply(lambda row: row['Quantit'] if row['Mvt'] == 131 else 0, axis=1)
    df['Sortie'] = df.apply(lambda row: row['Quantit'] if row['Mvt'] == 132 else 0, axis=1)

    # Grouper par article, mouvement et unité de quantité (UQ)
    df_grouped = df.groupby(['Article', 'UQ'], as_index=False).agg({'Entrée': 'sum', 'Sortie': 'sum'})
    return df_grouped

def process_blocage_data(df):
    """Traite les données de blocage/déblocage pour regrouper les quantités par article et mouvement."""
    # Convertir les colonnes en types appropriés
    df['Quantit'] = pd.to_numeric(df['Quantit'], errors='coerce')
    df['Mvt'] = df['Mvt'].astype(str)  # Convertir les codes de mouvement en chaînes de caractères

    # Filtrer les lignes valides
    df = df.dropna(subset=['Article', 'Mvt', 'Quantit']).copy()

    # Remplacer les numéros d'article par leurs noms
    df['Article'] = df['Article'].map(article_mapping).fillna("Inconnu")

    # Grouper par article et mouvement pour obtenir les totaux
    df_grouped = df.groupby(['Article', 'Mvt'], as_index=False).agg({'Quantit': 'sum'})
    return df_grouped