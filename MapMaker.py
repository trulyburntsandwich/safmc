# Map Maker


def create_blank_grid(grid_size = 26):
    # Create a grid init with 0 (free space)
    return [[0 for _ in range(grid_size)] for _ in range(grid_size)]

def place_tile(grid, row, col, tile_type):
    # Place a single tile on the grids
    if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
        grid[row][col] = tile_type
    else:
        print(f"Invalid coordinates: ({row}, {col})")

def place_area(grid, row, col, tile_type):
    # Place a rectangular area of tiles on the grid

    start_coords = [1, 6, 11, 16, 21]

    start_row = start_coords[row]
    start_col = start_coords[col]
    end_row = start_row + 4
    end_col = start_col + 4

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                grid[r][c] = tile_type

def print_grid(grid):
    # Pretty Print
    for row in grid:
        print(" ".join(str(cell) for cell in row))