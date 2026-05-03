import freqency_grid
import propagate
import numpy as np


def run():
    # Load the raw grid and geographic bounds from the input dataset.
    grid, min_lon, max_lon, min_lat, max_lat, time_values_grid = freqency_grid.get_grid()
    # Propagate the grid values to fill nearby empty cells.
    prob = propagate.propagate(grid)



    def next_position(grid, current_row, current_col, used):
        best_val = -1
        best_pos = (current_row, current_col)
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = current_row + dr, current_col + dc
                if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                    if grid[r, c] > best_val and (r, c) not in used:
                        best_val = grid[r, c]
                        best_pos = (r, c)
        
        used.add(best_pos)
        return best_pos, used

    used = set()

    flat_idx = np.argmax(prob)
    row_idx, col_idx = np.unravel_index(flat_idx, prob.shape)

    used.add((row_idx, col_idx))
    pos = (row_idx, col_idx)
    path = [pos]

    for step in range(10000):
        pos, used = next_position(prob, pos[0], pos[1], used)
        path.append(pos)
        print(f"current index: ({pos[0]}, {pos[1]})")

    print(f"Max index: ({row_idx}, {col_idx})")
    print(f"End index: ({pos[0]}, {pos[1]})")

    return path

if __name__ == "__main__":
    path = run()