import matplotlib.pyplot as plt
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap


white_to_red = LinearSegmentedColormap.from_list("wtr", ["white", "red"])

grid = freqency_grid.get_grid()
prob = propagate.propagate(grid)

fig, (ax1, ax2) = plt.subplots(1, 2)
im1 = ax1.imshow(grid,
            cmap=white_to_red,
            interpolation='nearest')
ax1.set_title("Frequency Grid")

fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

im2 = ax2.imshow(prob,
            cmap=white_to_red,
            interpolation='nearest')
ax2.set_title("Propagated Probability")

fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)


plt.show()
