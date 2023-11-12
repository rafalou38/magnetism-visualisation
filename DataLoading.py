import colorama
colorama.init(autoreset=True)
import numpy as np
import pandas as pd

def loadData(file: 'str'):
    print(f"Chargement de: \033[1;32m{file}\033[0m")
    # Chargement des données
    df = pd.read_csv(file)
    print(f"\t- Nombre de mesures: \033[1;36m{len(df)}\033[0m")
    maxX,maxY = 0,0
    for i in range(len(df)):
        if df['x'][i] > maxX:
            maxX = df['x'][i]
        if df['y'][i] > maxY:
            maxY = df['y'][i]
    print(f"\t- Dimension: \033[1;36m{maxX}x{maxY}\033[0m")

    # Mise en forme dans un tableau 
    grid = np.random.rand(maxX+1,maxY+1)
    for i in range(len(df)):
        grid[df['x'][i]][df['y'][i]] = df['v'][i]
        if df['x'][i] > maxX:
            maxX = df['x'][i]
        if df['y'][i] > maxY:
            maxY = df['y'][i]
    return grid