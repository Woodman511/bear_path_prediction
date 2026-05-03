import matplotlib.pyplot as plt
import graph_prob as gp
import path_find

gp.graph_data()
#gp.graph_data(gp.grid)

points = path_find.run()
x, y = zip(*points)
#gp.graph_data(points)

#gp.plt.show()
gp.ca_map.plot(x, y)
gp.ca_map.show()