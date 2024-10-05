#!/usr/bin/env python3
import rospy 
from geometry_msgs.msg import Twist
from mavros_msgs.srv import CommandBool, CommandTOL
class Drone:
    def __init__(self):
        self.armed = False
        self.landing = False
        rospy.init_node("Drone_controller",anonymous=True)
        self.vel_pub = rospy.Publisher("mavors/setpoint_velocity/cmd_vel", TwistStamped,queue_size=10)
        self.rate = rospy.Rate(10)

        self.armDrone(True)

    def armDrone(self,value:bool):
        rospy.wait_for_service("mavros/cmd/arming")
        rospy.wait_for_service("mavros/cmd/takeoff")
        try:
            arm_service = rospy.ServiceProxy("mavros/cmd/arming",CommandBool)
            takeoff_service = rospy.ServiceProxy("mavros/cmd/takeoff",CommandTOL)
            response = arm_service(value)
            response_takeoff = takeoff_service(altitude = 10)
            self.armed = True
            return response.success
        except rospy.ServiceException as e: 
            rospy.logerr(f"Service call falied : {e}")
            self.armed = False
            return False

    def sendControls(self,right_left_vel, forw_back_velocity,up_down_vel):
        vel_control = Twist()
        vel_control.linear.x = right_left_vel
        vel_control.linear.y = up_down_vel
        vel_control.linear.z = forw_back_velocity


        self.vel_pub.publish(vel_control)
        self.rate.sleep()

    def land(self):
        if self.landing:
            try:
                rospy.wait_for_service('/mavros/cmd/land')
                land_service = rospy.ServiceProxy("mavros/cmd/land",CommandTOL)
                response = land_service(altitude = 0)
                if response.success:
                    rospy.loginfo("Command sent successfully")
                    self.armDrone(False)
                    self.armed = False
                else:
                    rospy.loginfo("Failed to send Command")
            
            except rospy.ServiceException as e:
                rospy.logerr(f"Service call failed: {e}")
