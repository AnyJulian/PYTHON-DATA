import matplotlib.pyplot as plt
import numpy as np

# Générer des valeurs aléatoires pour les points
x = np.random.rand(50)  # 50 points aléatoires pour l'axe x
y = np.random.rand(50)  # 50 points aléatoires pour l'axe y

# Créer un nuage de points avec des triangles rouges
plt.scatter(x, y, c='red', marker='^')

# Afficher le graphique
plt.title("Nuage de points avec triangles rouges")
plt.xlabel("Axe X")
plt.ylabel("Axe Y")
plt.show()