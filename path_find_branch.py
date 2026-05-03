import freqency_grid
import propagate
import numpy as np


def run(users_pos_row = 108, users_pos_col = 271):
    # Load the raw grid and geographic bounds from the input dataset.
    grid, min_lon, max_lon, min_lat, max_lat, time_values_grid, land_mask, lat_matrix, lon_matrix = freqency_grid.get_grid()
    # Propagate the grid values to fill nearby empty cells.
    prob = propagate.propagate(grid)

    def next_position(current_row, current_col, grid = prob, branch = [[]], index = 0 ):
        neighbors = []
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = current_row + dr, current_col + dc
                if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                    val = grid[r, c]
                    pos = [r, c]
                    neighbors.append(pos)

        return neighbors    
    
    layers = [[ [[users_pos_row, users_pos_col]] ]]
    for i in range(20):
        next_layer = []
        for path in layers[-1]:  # each path in the last layer
            current_pos = path[-1]  # last position in the path
            neighbors = next_position(current_pos[0], current_pos[1], prob)
            for neighbor in neighbors:
                if neighbor not in path:
                    next_layer.append(path + [neighbor])  # extend the path
        
        vals = [sum(prob[pos[0], pos[1]] for pos in path) for path in next_layer]

        # Filter out paths below 10% of max value
        max_value = max(vals)
        scored = [(v, p) for v, p in zip(vals, next_layer) if v > max_value * 0.1]

        # Keep only top 100 paths by score
        scored.sort(key=lambda x: x[0], reverse=True)
        scored = scored[:1000]

        next_layer = [p for _, p in scored]
        vals = [v for v, _ in scored]

        layers.append(next_layer)
        #print(next_layer)
        #print()

            
    final_scored = [(sum(prob[pos[0], pos[1]] for pos in path), path) for path in layers[-1]]
    final_scored.sort(key=lambda x: x[0], reverse=True)

    top_3 = final_scored[:3]
    #for rank, (score, path) in enumerate(top_3, 1):
        #print(f"Rank {rank} | Score: {score:.4f} | Path: {path}")
    
    print(path for _, path in top_3)
    return [path for _, path in top_3]
    
run()
