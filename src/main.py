#!/usr/bin/env python3
from ROS_Controller import Drone

class Gesture_Controller:
    def __init__(self):
        self.fwd_bwd_vel = 0
        self.right_left_vel = 0
        self.up_down_vel = 0
        self.drone = Drone()

    def Controls(self,gesture):
        gesture_id = gesture
        print("Gesture_ID: ",gesture_id)

        if not self.drone.landing:
            if self.drone.armed:
                if gesture_id == 0: #forward
                    self.fwd_bwd_vel = 5
                elif gesture_id == 1:  # STOP
                    self.fwd_bwd_vel = self.up_down_vel = \
                        self.right_left_vel = 0
                if gesture_id == 5:  # Back
                    self.fwd_bwd_vel = -5

                elif gesture_id == 2:  # UP
                    self.up_down_vel = 5
                elif gesture_id == 4:  # DOWN
                    self.up_down_vel = -5

                elif gesture_id == 3:  # LAND
                    self.drone.landing = True
                    self.fwd_bwd_vel = self.up_down_vel = \
                        self.right_left_vel = 0
                    self.drone.land()

                elif gesture_id == 6: # LEFT
                    self.right_left_vel = 5
                elif gesture_id == 7: # RIGHT
                    self.right_left_vel = -5

                elif gesture_id == -1:
                    self.fwd_bwd_vel = self.up_down_vel = \
                        self.right_left_vel = 0

                self.drone.sendControls(self.right_left_vel, self.fwd_bwd_vel,
                                        self.up_down_vel)
            else:
                self.drone.armDrone(True)          

if __name__ == "__main__":
    controller = Gesture_Controller()
    for i in range(8):   
        gesture_id = int(input("Enter the id:" ))
        controller.Controls(gesture_id)