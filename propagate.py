import numpy as np

def propagate(matrix, land_mask=None):
    """
    Propagate probability values from seed cells to fill empty neighboring cells.
    This creates a smooth probability distribution across the grid.

    Args:
        matrix (numpy.ndarray): Input grid with probability values
        land_mask (numpy.ndarray): Boolean mask indicating land cells (True for land)

    Returns:
        numpy.ndarray: Propagated probability grid
    """
    if land_mask is None:
        land_mask = np.ones_like(matrix, dtype=bool)

    def equation(grid, n, m):
        """
        Calculate the propagated value for a cell based on its neighbors.
        Uses average of neighboring non-zero cells with a small penalty.

        Args:
            grid (numpy.ndarray): Current grid state
            n (int): Row index
            m (int): Column index

        Returns:
            float: Propagated value for the cell
        """
        if not land_mask[n, m]:
            return 0

        rows, cols = grid.shape
        total = 0
        times = 0

        # If cell already has a value, keep it
        if grid[n, m] != 0:
            return grid[n, m]

        # Sum values from non-zero neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = n + dr, m + dc
                if 0 <= r < rows and 0 <= c < cols:
                    if grid[r, c] != 0:
                        total += grid[r, c]
                        times += 1

        if times == 0:
            return 0

        # Return average with small penalty to prevent over-propagation
        return total / times - 0.05 / times

    # Iterative propagation: read from current, write to next_grid
    # This prevents new fills from influencing each other in the same wave
    current = matrix.astype(float).copy()
    filled = current != 0  # Track which cells are original seeds

    while True:
        next_grid = current.copy()
        changed = False

        # Process all cells
        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                if not filled[i, j]:  # Only touch unfilled cells
                    val = equation(current, i, j)
                    if val > 0:
                        next_grid[i, j] = val
                        filled[i, j] = True  # Mark as filled, never touch again
                        changed = True

        current = next_grid
        if not changed:
            break
            
    return current