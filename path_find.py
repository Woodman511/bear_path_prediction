import freqency_grid
import propagate
import numpy as np


def nearest_grid_cell(lat_matrix, lon_matrix, target_lat, target_lon):
    """Return the nearest grid cell row/col for the given lat/lon."""
    return freqency_grid.nearest_grid_cell(lat_matrix, lon_matrix, target_lat, target_lon)


def run(user_start_lon=None, user_start_lat=None):
    """
    Run the path finding algorithm to simulate bear movement.

    Args:
        user_start_lon (float|int|None): Starting longitude, or None to use max-probability cell.
        user_start_lat (float|int|None): Starting latitude, or None to use max-probability cell.

    Returns:
        list: List of (row, col) tuples representing the path
    """
    # Load the raw grid and geographic bounds from the input dataset.
    grid, min_lon, max_lon, min_lat, max_lat, time_values_grid, land_mask, lat_matrix, lon_matrix = freqency_grid.get_grid()
    # Propagate the grid values to fill nearby empty cells.
    prob = propagate.propagate(grid, land_mask=land_mask)

    def next_position(grid, current_row, current_col, used):
        """
        Find the next position with the highest probability adjacent to the current position.

        Args:
            grid (numpy.ndarray): The probability grid
            current_row (int): Current row index
            current_col (int): Current column index
            used (set): Set of already visited positions

        Returns:
            tuple: (next_position, updated_used_set)
        """
        best_val = -1
        best_pos = (current_row, current_col)
        
        # Check all 8 adjacent cells
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = current_row + dr, current_col + dc
                if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                    if grid[r, c] > best_val and (r, c) not in used:
                        best_val = grid[r, c]
                        best_pos = (r, c)
                        # Slightly reduce the value to discourage revisiting
                        grid[r, c] -= 0.1
        # Mark position as used (currently commented out)
        #used.add(best_pos)
        return best_pos, used

    # Initialize used positions set
    used = set()

    # Find the starting position (maximum probability) if no explicit start coordinate is provided.
    flat_idx = np.argmax(prob)
    if user_start_lon is None or user_start_lat is None:
        if not (user_start_lon is None and user_start_lat is None):
            raise ValueError("Both user_start_lon and user_start_lat must be provided or both must be None")
        row_idx, col_idx = np.unravel_index(flat_idx, prob.shape)
    else:
        row_idx, col_idx = freqency_grid.nearest_grid_cell(lat_matrix, lon_matrix, user_start_lat, user_start_lon)

    # Add starting position to used set
    used.add((row_idx, col_idx))
    pos = (row_idx, col_idx)
    path = [pos]

    # Generate path for 10000 steps
    for step in range(100):
        pos, used = next_position(prob, pos[0], pos[1], used)
        path.append(pos)
        
        if step % 100 == 0:
            grid, min_lon, max_lon, min_lat, max_lat, time_values_grid, land_mask, lat_matrix, lon_matrix = freqency_grid.get_grid(step)
            prob = propagate.propagate(grid, land_mask=land_mask)
        

    print(f"Max index: ({row_idx}, {col_idx})")
    print(f"End index: ({pos[0]}, {pos[1]})")

    return path

if __name__ == "__main__":
    path = run()