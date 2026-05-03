import numpy as np


def propagate(matrix):
    def equation(grid, n, m):
        rows, cols = grid.shape
        total = 0
        times = 0

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = n + dr, m + dc
                if 0 <= r < rows and 0 <= c < cols:
                    if grid[r, c] > 0:  # ignore negatives and zeros
                        total += grid[r, c]
                        times += 1

        if times == 0:
            return 0
        return total / times - 0.05 / times

    current = matrix.astype(float).copy()
    negative_mask = current < 0  # remember where negatives are
    filled = current != 0        # seeds are non-zero (positive or negative)

    while True:
        next_grid = current.copy()
        changed = False

        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                if not filled[i, j]:
                    val = equation(current, i, j)
                    if val > 0:
                        next_grid[i, j] = val
                    filled[i, j] = True
                    changed = True

        # restore negatives to original values
        next_grid[negative_mask] = matrix[negative_mask]
        current = next_grid
        if not changed:
            break

    return current