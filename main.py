# import Slam as slam
import MapMaker as map
import TelloDrone as tello
import ImageRecognition as IMrecog


# TILE VALUE REFERENCE:
# 0 = Free space
# 1 = Hospital A 
# 2 = Hospital B 
# 3 = Checkpoint 
# 4 = Medical Evacuation 
# 5 = HDB 
# 6 = Arial Photograph Y
# 7 = Restricted Area

# Create the grid
grid = map.create_blank_grid()

# Place Hospital A (1)
map.place_area(grid, 0, 1, 1)

# Place Hospital B (2)
map.place_area(grid, 2, 1, 2)

# Place Checkpoint (3)
map.place_area(grid, 1, 1, 3)

# Place Medical Evacuation (4)
map.place_area(grid, 2, 0, 4)

# Place HDB (5)
map.place_area(grid, 0, 4, 5)
map.place_area(grid, 1, 3, 5)
map.place_area(grid, 2, 2, 5)
map.place_area(grid, 3, 1, 5)

# Place Arial Photograph Y (only choose 2 locations) (6)
map.place_area(grid, 4, 1, 6)
map.place_area(grid, 4, 3, 6)

# Place restricted area (7)
map.place_area(grid, 3, 3, 7)

def hospital():
    pass

# def main(): 
#     slam.drone.takeoff()
#     slam.drone.move_forward(23)
#     slam.drone.move_right(13)

#     slam.drone.move_forward(20)

#     slam.drone.land()
#     slam.drone.end()

if __name__  == "__main__":
    map.print_grid(grid)
    # main()