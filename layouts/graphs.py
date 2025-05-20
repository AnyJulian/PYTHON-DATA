import plotly.express as px

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