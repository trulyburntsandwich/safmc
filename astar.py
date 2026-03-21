import math
import heapq

class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parentRow = 0
        # Parent cell's column index
        self.parentColumn = 0
        # Total cost of the cell (g + h)
        self.totalCost = float('inf')
        # Cost from start to this cell
        self.travelCost = float('inf')
        # Heuristic cost from this cell to destination
        self.hueristic = 0

# Grid Size
ROW = 26
COL = 26

# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] in [0, "0", "6", "7", "8", "9", "-"]

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
    print("The Path is ")
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parentRow == row and cell_details[row][col].parentColumn == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parentRow
        temp_col = cell_details[row][col].parentColumn
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    for i in path:
        print("->", i, end=" ")
    print()


def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    row = src[0]
    column = src[1]
    cell_details[row][column].f = 0
    cell_details[row][column].g = 0
    cell_details[row][column].h = 0
    cell_details[row][column].parentRow = row
    cell_details[row][column].parentColumn = column

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, row, column))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        poppedList = heapq.heappop(open_list)

        # Mark the cell as visited
        row = poppedList[1]
        column = poppedList[2]
        closed_list[row][column] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_row = row + dir[0]
            new_column = column + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_row, new_column) and is_unblocked(grid, new_row, new_column) and not closed_list[new_row][new_column]:
                # If the successor is the destination
                if is_destination(new_row, new_column, dest):
                    # Set the parent of the destination cell
                    cell_details[new_row][new_column].parentRow = row
                    cell_details[new_row][new_column].parentColumn = column
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest)
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    travelCost_new = cell_details[row][column].g + 1.0
                    hueristic_new = calculate_h_value(new_row, new_column, dest)
                    totalCost_new = travelCost_new + hueristic_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_row][new_column].f == float('inf') or cell_details[new_row][new_column].f > totalCost_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (totalCost_new, new_row, new_column))
                        # Update the cell details
                        cell_details[new_row][new_column].f = totalCost_new
                        cell_details[new_row][new_column].g = travelCost_new
                        cell_details[new_row][new_column].h = hueristic_new
                        cell_details[new_row][new_column].parentRow = row
                        cell_details[new_row][new_column].parentColumn = column

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

# Map Maker
def create_blank_grid():
    """Create a blank 25x25 grid with all 0s (free space)"""
    return [[0 for _ in range(25)] for _ in range(25)]

def place_tile(grid, row, col, tile_type):
    """Place a single tile on the grid"""
    if 0 <= row < 25 and 0 <= col < 25:
        grid[row][col] = tile_type
    else:
        print(f"Invalid coordinates: ({row}, {col})")

def place_area(grid, start_row, start_col, end_row, end_col, tile_type):
    """Place a rectangular area of tiles on the grid"""
    for r in range(start_row, end_row + 1):
        for c in range(start_col, end_col + 1):
            if 0 <= r < 25 and 0 <= c < 25:
                grid[r][c] = tile_type

def print_grid(grid):
    """Print the grid in terminal"""
    for row in grid:
        print(" ".join(str(cell) for cell in row))



# Driver Code
def main():
    # TILE VALUE REFERENCE:
    # 0 = Drone Pathway (drone CAN move through)
    # 1 = Hospital A (blocks movement)
    # 2 = Hospital B (blocks movement)
    # 3 = Checkpoint (blocks movement)
    # 4 = Medical Evacuation (blocks movement)
    # 5 = HDB (blocks movement)
    # 6 = Delivery (drone CAN move through)
    # 7 = Arial Photograph Y (drone CAN move through)
    # 8 = Image (drone CAN move through)
    # 9 = Restricted Area (drone CAN move through)
    # "-" = Free Space (drone CAN move through)

    # EXAMPLE: Create grid using helper functions
    grid = create_blank_grid()
    
    # Place Hospital A
    place_area(grid, 2, 7, 6, 11, 1)

    # Place Checkpoint
    place_area(grid, 7, 7, 11, 11, 3)

    # Place Hospital B
    place_area(grid, 12, 7, 16, 11, 2)
    
    # Place Medical Evacuation
    place_area(grid, 11, 1, 14, 4, 5)
    
    # Place delivery locations - drone CAN move through (7)
    place_area(grid, 21, 6, 24, 9, 7)
    
    # Place HDB locations - drone CAN move through (6)
    place_area(grid, 11, 11, 14, 14, 6)
    
    # Place restricted area - drone CAN move through (9)
    place_area(grid, 16, 16, 19, 19, 9)
    
    # Place image locations - drone CAN move through (8)
    place_tile(grid, 6, 24, 8)
    place_tile(grid, 16, 24, 8)
    place_tile(grid, 24, 8, 8)

    # Define the source and destination
    src = [0, 0]
    dest = [24, 24]


if __name__ == "__main__":
    main()