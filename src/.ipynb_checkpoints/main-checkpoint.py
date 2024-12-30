#!/usr/bin/env python3
from ROS_Controller import Drone
import rospy

class Gesture_Controller:
    def __init__(self):
        self.drone = Drone()

    def Controls(self,gesture):
        gesture_id = gesture
        print("Gesture_ID: ",gesture_id)

        if gesture_id == 0: #arm
            self.drone.arm_drone(True)
        elif gesture_id == 1: #takeoff
            self.drone.takeoff_drone()
        elif gesture_id == -1: #Land
            self.drone.land_drone()
        elif gesture_id == 2:  # STOP
            self.drone.velocity_cmd(x_vel=0, y_vel=0,z_vel=0)
        elif gesture_id == 3:  # Back
            y_vel = -1
            self.drone.velocity_cmd(y_vel=-1)
        
        elif gesture_id == 4:  # Forward
            self.drone.velocity_cmd(y_vel=1)

        elif gesture_id == 5:  # Up
            self.drone.velocity_cmd(z_vel=1)
        
        elif gesture_id == 6:  # Down
            self.drone.velocity_cmd(z_vel=-1)

        elif gesture_id == 7: # LEFT
            self.drone.velocity_cmd(x_vel=-1)

        elif gesture_id == 8: # RIGHT
            self.drone.velocity_cmd(x_vel=1)
        else:
            rospy.loginfo("Invalid gesture_id")

if __name__ == "__main__":
    controller = Gesture_Controller()
    while(True):   
        gesture_id = int(input("Enter the id:" ))
        controller.Controls(gesture_id)