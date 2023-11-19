import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FuncFormatter
import DataLoading as DL
import os


def view(file):
    grid, minV, maxV, res = DL.loadData("data/" + file)

    colors = [
        (92 / 255, 89 / 255, 255 / 255),
        (1, 1, 1),
        (255 / 255, 100 / 255, 89 / 255),
    ]  # Blue, White, Red
    n_bins = 1000  # Number of bins
    custom_cmap = LinearSegmentedColormap.from_list("custom_coolwarm", colors, N=n_bins)

    # plt.figure(figsize=(9, 6))
    plt.figure()

    plt.subplot(1, 2, 1)
    plt.title("Données brutes")
    plt.imshow(
        grid,
        cmap=custom_cmap,
        vmin=-max(abs(minV), abs(maxV)),
        vmax=max(abs(minV), abs(maxV)),
        extent=[0, 1.5 * (grid.shape[1]*res) / 100, 0,2.3 * (grid.shape[0]*res) / 100],
    )
    plt.grid(color=(1,1,1), linestyle='-', linewidth=0.2)  # Add a light grid
    plt.colorbar()
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.5))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))
    plt.xlabel('X (cm)')
    plt.ylabel('Y (cm)')

    plt.subplot(1, 2, 2)
    plt.title("Données interpolés")
    plt.imshow(
        grid,
        cmap=custom_cmap,
        interpolation="bicubic",
        vmin=-max(abs(minV), abs(maxV)),
        vmax=max(abs(minV), abs(maxV)),
        extent=[0, 1.5 * (grid.shape[1]*res) / 100, 0,2.3 * (grid.shape[0]*res) / 100],
    )
    plt.grid(color=(1,1,1), linestyle='-', linewidth=0.2)  # Add a light grid
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.5))
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))
    plt.xlabel('X (cm)')
    plt.ylabel('Y (cm)')
    plt.colorbar()
    plt.tight_layout()

    # Sauvegarde image
    plt.savefig("out/" + file + ".png", dpi=300)
    print("Image sauvegardé: \033[1;32mout.png\033[0m")

    # Affichage fenêtre
    # plt.show()


if __name__ == "__main__":
    # view("3-hors-champ.csv")
    for file in os.listdir("data"):
        if file.endswith(".csv"):
            print(file)
            view(file)
