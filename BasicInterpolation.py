import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

import numpy as np
import pandas as pd

# Chargement des données
df = pd.read_csv('data.csv')
minV, maxV = -3,3
maxX,maxY = 0,0
for i in range(len(df)):
    if df['x'][i] > maxX:
        maxX = df['x'][i]
    if df['y'][i] > maxY:
        maxY = df['y'][i]

# Mise en forme dans un tableau 
grid = np.random.rand(maxX+1,maxY+1)
for i in range(len(df)):
    grid[df['x'][i]][df['y'][i]] = (df['v'][i] - minV) / (maxV - minV)
    if df['x'][i] > maxX:
        maxX = df['x'][i]
    if df['y'][i] > maxY:
        maxY = df['y'][i]
print(grid)

plt.figure(figsize=(9, 3))

plt.subplot(1, 2, 1)
plt.title('Données brutes')
plt.imshow(grid, cmap='coolwarm')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.title('Données interpolés')
plt.imshow(grid, cmap='coolwarm', interpolation='gaussian')
plt.colorbar()
plt.tight_layout()

# Sauvegarde image
mpl.rcParams['figure.dpi'] = 300
plt.savefig('out.png', dpi=300)

# Affichage fenêtre
plt.show()
