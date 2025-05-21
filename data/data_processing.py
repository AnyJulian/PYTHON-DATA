import pandas as pd
from utils.constants import article_mapping
import holidays

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

def process_sales_daily_data(df):
    """Nettoie et transforme les données de ventes."""
    # Nettoyer la colonne Quantité
    df['Quantité'] = df['Quantité'].str.strip()
    df['Quantité'] = pd.to_numeric(df['Quantité'], errors='coerce')
    df = df.dropna(subset=['Quantité'])

    # Convertir les dates avec le bon format
    df.loc[:, 'Date Comptable'] = pd.to_datetime(df['Date Comptable'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Date Comptable'])

    # Grouper les données par jour et additionner les quantités
    df_daily = df.groupby('Date Comptable').agg({'Quantité': 'sum'}).reset_index()

    # Générer une plage complète de dates
    all_dates = pd.date_range(start=df_daily['Date Comptable'].min(),
                              end=df_daily['Date Comptable'].max(),
                              freq='d')

    # Supprimer les week-ends
    all_dates = all_dates[~all_dates.weekday.isin([5, 6])]

    # Supprimer les jours fériés
    fr_holidays = holidays.France(years=all_dates.year.unique())
    
    # Convertir les jours fériés en datetime64[ns]
    fr_holidays = pd.to_datetime(list(fr_holidays), errors='coerce')

    # Supprimer les jours fériés
    all_dates = all_dates[~all_dates.isin(fr_holidays)]

    # Fusionner avec les données existantes pour inclure toutes les dates
    df_daily = pd.DataFrame({'Date Comptable': all_dates}).merge(
        df_daily, on='Date Comptable', how='left'
    )

    # Remplir les quantités manquantes avec 0
    df_daily['Quantité'] = df_daily['Quantité'].fillna(0)

    return df_daily