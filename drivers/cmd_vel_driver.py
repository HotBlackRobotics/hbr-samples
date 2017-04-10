import dotbot_ros
from gpiozero import Robot
from geometry_msgs.msg import Twist

class Node(dotbot_ros.DotbotNode):
    node_name = 'cmd_vel_driver'
    left_wheel = (16, 19)
    right_wheel = (20, 26)

    rotation_factor = 2.0
    translation_factor = 1.0/10

    def setup(self):
        self.robot = Robot(left=left_wheel, right=right_wheel)
        dotbot_ros.Subscriber("cmd_vel", Twist, self.on_cmd_vel)

    def on_cmd_vel(self, cmd_vel):
        v_dx = translation_factor*cmd_vel.linear.x + rotation_factor*cmd_vel.angular.z
        v_sx = translation_factor*cmd_vel.linear.x - rotation_factor*cmd_vel.angular.z

        # Saturazione
        if v_dx > 1.0: v_dx = 1.0
        elif v_dx < -1.0: v_dx = -1.0
        if v_sx > 1.0: v_sx = 1.0
        elif v_sx < -1.0: v_sx = -1.0

        #controllo del robot
        self.robot.value = (v_dx, v_sx)
