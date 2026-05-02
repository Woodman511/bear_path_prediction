import numpy as np


def propagate(matrix):

    def equation(grid, n, m):
        rows, cols = grid.shape
        total = 0
        times = 0

        if grid[n, m] != 0:
            return grid[n, m]

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

        return total / times - 0.1 / times


    # Each pass reads from `current`, writes into `next_grid`
    # so new fills never influence each other in the same wave
    current = matrix.copy()
    while True:
        next_grid = current.copy()
        changed = False

        for i in range(current.shape[0]):
            for j in range(current.shape[1]):
                if current[i, j] == 0:
                    val = equation(current, i, j)
                    if val > 0:
                        next_grid[i, j] = val
                        changed = True

        current = next_grid
        if not changed:
            break

    np.set_printoptions(precision=3, suppress=True)
    print(current)
