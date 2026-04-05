from djitellopy import Tello
import cv2

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

# Test
def test():
    drone = TelloDrone()

    drone.takeoff()

    drone.move_forward()

    drone.land()
    drone.end()