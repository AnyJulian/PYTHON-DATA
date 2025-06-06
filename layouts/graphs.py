import plotly.express as px
import plotly.graph_objects as go

def create_silo_graph(df2):
    """Crée le graphique pour l'évolution des niveaux des silos."""
    return px.line(
        df2,
        x='Date',
        y=['silo12', 'silo13', 'silo14', 'silo15'],
        title="Évolution des niveaux des silos au fil du temps",
        labels={'value': 'Niveau', 'variable': 'Silo'}
    )

def create_air_fresh_graph(df3):
    """Crée le graphique pour l'évolution des niveaux d'air frais."""
    return px.line(
        df3,
        x='Date',
        y='Air Frais',
        title="Évolution des niveaux d'air frais rentrant au fil du temps",
        labels={'value': 'Niveau'}
    )

def create_stock_graph(df_stock):
    """Crée un graphique pour les mouvements de stock (entrées et sorties)."""
    if 'Entrée' not in df_stock.columns or 'Sortie' not in df_stock.columns:
        raise ValueError("Les colonnes 'Entrée' et 'Sortie' sont manquantes dans les données de stock.")

    return px.bar(
        df_stock,
        x='Article',
        y=['Entrée', 'Sortie'],
        title="Mouvements de stock par article",
        labels={'value': 'Quantité', 'variable': 'Type de mouvement', 'Article': 'Article'},
        barmode='group',  # Affiche les barres côte à côte
        color_discrete_map={'Entrée': 'green', 'Sortie': 'red'}  # Couleurs personnalisées
    )

def create_blocage_graph(df_blocage):
    """Crée un graphique pour les blocages et déblocages de stock."""
    return px.bar(
        df_blocage,
        x='Article',
        y='Quantit',
        color='Mvt',  # Les segments de la barre représentent les différents codes de mouvement
        title="Blocages et déblocages de stock par article",
        labels={'Quantit': 'Quantité', 'Mvt': 'Code Mouvement', 'Article': 'Article'},
        barmode='stack',  # Barres empilées
        color_discrete_map={
            '321': 'darkgreen',  # Vert foncé
            '322': 'lightgreen',  # Vert clair
            '343': 'darkred',  # Rouge foncé
            '344': 'lightcoral'  # Rouge clair
        }
    )

def create_sales_graph(df_sales_daily):
    """Crée un graphique des ventes historiques."""
    fig = go.Figure()

    # Historique des ventes (toutes les dates sauf week-ends et jours fériés)
    fig.add_trace(go.Scatter(
        x=df_sales_daily['Date Comptable'],
        y=df_sales_daily['Quantité'],
        mode='lines',
        name='Historique des ventes'
    ))

    fig.update_layout(
        title="Graphique des ventes historiques (sans week-ends et jours fériés)",
        xaxis_title="Date",
        yaxis_title="Quantité",
        template="plotly_white"
    )

    return fig

def create_air_fresh_prediction_graph(df, model):
    """Crée un graphique pour les prédictions de consommation électrique."""
    # Prédire les coûts en fonction des niveaux d'air frais
    df['Coût Prédit (€)'] = model.predict(df[['Air Frais']])

    # Créer le graphique
    fig = go.Figure()

    # Ajouter les données réelles
    fig.add_trace(go.Scatter(
        x=df['Air Frais'],
        y=df['Coût Total (€)'],
        mode='markers',
        name='Données Réelles'
    ))

    # Ajouter les prédictions
    fig.add_trace(go.Scatter(
        x=df['Air Frais'],
        y=df['Coût Prédit (€)'],
        mode='lines',
        name='Prédictions'
    ))

    fig.update_layout(
        title="Prédictions de Consommation Électrique en Fonction de l'Air Frais",
        xaxis_title="Air Frais",
        yaxis_title="Coût Total (€)",
        template="plotly_white"
    )

    return fig

def create_air_fresh_graph_with_cost(df):
    """Crée un graphique pour l'évolution des niveaux d'air frais et du coût prédit."""
    fig = go.Figure()

    # Ajouter la courbe des niveaux d'air frais
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Air Frais'],
        mode='lines',
        name='Niveaux d\'Air Frais',
        line=dict(color='blue')
    ))

    # Ajouter la courbe du coût prédit
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Coût Prédit (€)'],
        mode='lines',
        name='Coût Prédit (€)',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title="Évolution des Niveaux d'Air Frais et du Coût Prédit",
        xaxis_title="Date",
        yaxis_title="Valeurs",
        template="plotly_white",
        legend=dict(x=0, y=1, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(0,0,0,0)')
    )

    return fig