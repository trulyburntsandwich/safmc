from djitellopy import Tello
import time
import cv2

# Define locations on the 25x25 grid
locations = {
    'hospital_a': (6, 8),
    'hospital_b': (12, 10),
    'delivery_1': (3, 5),
    'delivery_2': (8, 20),
    'delivery_3': (18, 15),
    'qr_1': (2, 2),
    'qr_2': (22, 22),
    'photo_1': (10, 5),
    'photo_2': (15, 20),
}

class TelloDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()

    ####################################################
    #  Start/Stop                    
    ####################################################

    def takeoff(self):
        self.tello.takeoff()

    def land(self):
        self.tello.land()

    def end(self):
        self.tello.end()

    ####################################################
    #  Movement Functions                               
    ####################################################

    # Basic Movement
    def move_forward(self, distance):
        self.tello.move_forward(distance)

    def move_backward(self, distance):
        self.tello.move_back(distance)

    def move_left(self, distance):
        self.tello.move_left(distance)

    def move_right(self, distance):
        self.tello.move_right(distance)

    def move_up(self, distance):
        self.tello.move_up(distance)

    def move_down(self, distance):
        self.tello.move_down(distance)

    # Drone Flip
    def flip_forward(self):
        self.tello.flip_forward()

    def flip_backward(self):
        self.tello.flip_back()

    def flip_left(self):
        self.tello.flip_left()

    def flip_right(self):
        self.tello.flip_right()

    # Rotation
    def turn_right(self, degrees):
        self.tello.rotate_clockwise(degrees)

    def turn_left(self, degrees):
        self.tello.rotate_counter_clockwise(degrees)

    ####################################################
    #  Camera                                           
    ####################################################

    def take_photo(self, saveName: str, direction: str = "forward"):
        if direction == "forward":
            self.tello.set_video_direction(Tello.CAMERA_FORWARD)

        elif direction == "downward":
            self.tello.set_video_direction(Tello.CAMERA_DOWNWARD)

        self.tello.streamon()
        frameRead = self.tello.get_frame_read()

        self.tello.streamoff()

        path = f"./media/{saveName}.png"
        cv2.imwrite(path, frameRead.frame)

drone = TelloDrone()

# drone.takeoff()

# Example: Find path from (0, 0) to hospital A
# path = drone.path_find((0, 0), locations['hospital_a'])

# Example: Find path using location names
# path = drone.path_find((0, 0), (6, 8))

drone.take_photo("photo", "downward")

# drone.land()
drone.end()