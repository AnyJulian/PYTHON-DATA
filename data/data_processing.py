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