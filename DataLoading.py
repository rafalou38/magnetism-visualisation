import colorama
colorama.init(autoreset=True)
import numpy as np
import pandas as pd


def loadData(file: 'str'):
    print(f"Chargement de: \033[1;32m{file}\033[0m")
    # Chargement des données
    df = pd.read_csv(file)
    res = df["y"][1] - df["y"][0]

    print(f"\t- Nombre de mesures: \033[1;36m{len(df)}\033[0m")
    print(f"\t- Resolution: \033[1;36m{res}\033[0m")
    maxX,maxY = 0,0
    minV,maxV = 1000,0
    for i in range(len(df)):
        if(minV > df['v'][i]): minV = df['v'][i]
        if(maxV < df['v'][i]): maxV = df['v'][i]
        if df['x'][i]//res > maxX:
            maxX = df['x'][i]//res
        if df['y'][i]//res > maxY:
            maxY = df['y'][i]//res
    print(f"\t- Dimension: \033[1;36m{maxX}x{maxY}\033[0m")

    # Mise en forme dans un tableau 
    grid = np.random.rand(maxX+1,maxY+1)

    print(minV, maxV)
    for i in range(len(df)):
        grid[df['x'][i]//res][df['y'][i]//res] = df['v'][i]
        # grid[df['x'][i]//res][df['y'][i]//res] = (((df['v'][i] - minV) / (maxV - minV)) * 8) - 4
        if df['x'][i]//res > maxX:
            maxX = df['x'][i]//res
        if df['y'][i]//res > maxY:
            maxY = df['y'][i]//res
    return grid, minV,maxV, res