import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.interpolate import griddata

import DataLoading as DL

INTERPOLATION_FACTOR = 10

grid = DL.loadData("data.csv")

# Interpolation
x, y = np.meshgrid(np.arange(grid.shape[1]), np.arange(grid.shape[0]))
xi, yi = np.meshgrid(
    np.linspace(0, grid.shape[1]-1, grid.shape[1] * INTERPOLATION_FACTOR),
    np.linspace(0, grid.shape[0]-1, grid.shape[0] * INTERPOLATION_FACTOR))
zi = griddata((x.flatten(), y.flatten()), grid.flatten(), (xi, yi), method='cubic')



# Affichage de la surface
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
plt.title(f'Données interpolés (x{INTERPOLATION_FACTOR})')
plt.tight_layout()

surf = ax.plot_surface(xi, yi, zi, cmap="coolwarm",
                       linewidth=0, antialiased=False)

ax.set_zlim(-5, 5)
# Précisions axe z
ax.zaxis.set_major_formatter('{x:.02f}')

fig.colorbar(surf, shrink=0.5, aspect=5)


def sauveAnim():
    def update(frame):
        ax.view_init(elev=20, azim=frame)
        return surf,

    ani = FuncAnimation(fig, update, frames=np.arange(0, 362, 2), interval=50, blit=True)

    ani.save('animation.gif', writer='pillow', fps=60)
    print("Image sauvegardé: \033[1;32animation.mp4\033[0m")

def sauveImg():
    plt.savefig('out.png', dpi=300)
    print("Image sauvegardé: \033[1;32mout.png\033[0m")

sauveImg()
# Affichage fenêtre
plt.show()
