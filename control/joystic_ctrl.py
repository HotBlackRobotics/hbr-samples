import dotbot_ros
from gpiozero import Robot
from geometry_msgs.msg import Vector3
import sys

class Node(dotbot_ros.DotbotNode):
    node_name = 'joystick_ctrl'
    rescaling_factor = -1.0/600

    def setup(self):
        self.robot = Robot(left=(16, 19), right=(20, 26))
        dotbot_ros.Subscriber("joy", Vector3, self.on_joy)

    def on_joy(self, msg):
        v_dx = rescaling_factor*(msg.y - msg.x)
        v_sx = rescaling_factor*(msg.y + msg.x)

        # Saturazione
        if v_dx > 1.0: v_dx = 1.0
        elif v_dx < -1.0: v_dx = -1.0
        if v_sx > 1.0: v_sx = 1.0
        elif v_sx < -1.0: v_sx = -1.0

        #controllo del robot
        self.robot.value = (v_dx, v_sx)
