import matplotlib.pyplot as plt
import freqency_grid
import propagate
from matplotlib.colors import LinearSegmentedColormap


white_to_red = LinearSegmentedColormap.from_list("wtr", ["white", "red"])

grid = freqency_grid.get_grid()
prob = propagate.propagate(grid)

plt.imshow(prob,
            cmap=white_to_red,
            interpolation='nearest')
plt.colorbar()
plt.show()