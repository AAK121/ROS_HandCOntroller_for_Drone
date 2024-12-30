#!\usr/bin/env python3

import rospy 
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandBoolRequest, CommandTOL, CommandTOLRequest
from mavros_msgs.srv import SetMode, SetModeRequest
from mavros_msgs.msg import State
from nav_msgs.msg import Odometry

class Drone:
    def __init__(self):
        self.armed = False

        rospy.init_node("drone_controller",anonymous=True)
        rospy.wait_for_service('/mavros/cmd/land')
        rospy.wait_for_service('/mavros/cmd/takeoff')
        rospy.wait_for_service('/mavros/cmd/arming')
        rospy.wait_for_service('/mavros/set_mode')


        self.land_service = rospy.ServiceProxy('/mavros/cmd/land',CommandTOL)
        self.takeoff_service = rospy.ServiceProxy('/mavros/cmd/takeoff',CommandTOL)
        self.arm_service = rospy.ServiceProxy('/mavros/cmd/arming',CommandBool)
        self.set_mode_service = rospy.ServiceProxy('/mavros/set_mode',SetMode)

        self.vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped',Twist,queue_size=10)

        self.cmd_vel = Twist()
    def land_drone(self):
        try:
            land_req = CommandTOLRequest()
            land_req.altitude = 0
            response = self.land_service(land_req)

            if response.success:
                rospy.loginfo("Landing was done successfully")
            else:
                rospy.logwarn("Landing was unsuccessfull")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed as {e}")
        
        self.armed = False

    def arm_drone(self,value:bool):
        self.set_flight_mode("GUIDED")
        try:
            arm_req = CommandBoolRequest()
            arm_req.value = value
            response = self.arm_service(arm_req)
            if response.success:
                rospy.loginfo("Drone Armed Successfully")
            else:
                rospy.logwarn("Drone arming unsuccessfull")

        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed as {e}")

    def set_flight_mode(self,mode):
        try: 
            mode_req = SetModeRequest()
            mode_req.custom_mode = mode
            response = self.set_mode_service(mode_req)
            if response.mode_sent:
                rospy.loginfo(f"Mode set successfully to {mode}")
            else:
                rospy.logwarn("Mode not set")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed as {e}")

    def takeoff_drone(self,altitude = 5):
        try:
            takeoff_req = CommandTOLRequest()
            takeoff_req.altitude = altitude
            response = self.takeoff_service(takeoff_req)
            if response.success:
                rospy.loginfo("Takeoff was successfull")
            else:
                rospy.logwarn("Takeoff was unsuccessfull")
        except rospy.ServiceException as e:
            rospy.logwarn(f"Service call failed as {e}")
    
    def velocity_cmd(self,x_vel=0,y_vel=0,z_vel=0):
        try:
            self.cmd_vel.linear.x = x_vel
            self.cmd_vel.linear.y = y_vel
            self.cmd_vel.linear.z = z_vel
            self.vel_pub.publish(self.cmd_vel)
            rospy.loginfo(f"Velocity commands sent successfully")
            rospy.loginfo(f"x : {x_vel} \n y: {y_vel} \n z: {z_vel}")
        except rospy.ServiceException as e:
            rospy.logerr(f"Service call failed as {e}")
