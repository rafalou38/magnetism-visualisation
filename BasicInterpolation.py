import matplotlib.pyplot as plt
import DataLoading as DL

grid = DL.loadData("data.csv")

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
plt.savefig('out.png', dpi=300)
print("Image sauvegardé: \033[1;32mout.png\033[0m")

# Affichage fenêtre
plt.show()
