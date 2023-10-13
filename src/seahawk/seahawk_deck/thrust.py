'''
thrust.py

Calculate correct output of motors and output it on /drive/motors

Copyright (C) 2022-2023 Cabrillo Robotics Club

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Cabrillo Robotics Club
6500 Soquel Drive Aptos, CA 95003
cabrillorobotics@gmail.com
'''
import sys 

import rclpy

from rclpy.node import Node 

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

import numpy as np

class Thrust(Node):
    """
    Class that implements the kinematics.
    """

    def __init__(self):
        """Initialize this node"""
        super().__init__('thrust')

        root3 = 1/math.sqrt(3)
        

        self.motor_config = [
            [root3, root3, root3, root3, -root3, -root3, -root3, -root3], 
            [-root3, root3, -root3, root3, -root3, root3, -root3, root3], 
            [root3, root3, -root3, -root3, root3, root3, -root3, -root3],
            [root3, -root3, -root3, root3, root3, -root3, -root3, root3],
            [-2*root3, -2*root3, 2*root3, 2*root3, 2*root3, 2*root3, -2*root3, -2*root3],
            [-1/root3, 1/root3, -1/root3, 1/root3, 1/root3, -1/root3, 1/root3, -1/root3]
        ]
        self.inverse_config = np.linalg.pinv(motor_config, rcond=1e-15, hermitian=False)

        self.subscription = self.create_subscription(Twist, 'drive/twist', self._callback, 10)
        self.motor_pub = self.create_publisher(Float32MultiArray, 'drive/motors', 10)
        

    def _callback(self, twist_msg):
        """Called every time the twist publishes a message."""

        # Convert the X,Y,Z,R,P,Y to thrust settings for each motor. 
        motor_msg = Float32MultiArray()
        # +1 = Full thrust, Forwards
        #  0 = Off
        # -1 = Full thrust, Backwards
        # Even are on bottom
        # 45° angle(π/4)
        # ^FRONT^
        # 6/. .\0
        # 4\^ ^/2
        # Odd are on top; thrust forward is up
        # 35° angle(7π/36)
        # ^FRONT^
        #  7   1
        #  5   3

        # Convert Twist to single vector for multiplication
        twist_array = [
            twist_msg.linear.x,
            twist_msg.linear.y,
            twist_msg.linear.z,
            twist_msg.angular.x,
            twist_msg.angular.y,
            twist_msg.angular.z
        ]

        # Multiply twist with inverse of motor config to get motor effort values
        motor_msg.data = np.matmul(self.inverse_config, twist_array)

        self.motor_pub.publish(motor_msg)


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(Thrust())
    rclpy.shutdown()    


if __name__ == '__main__':
    main(sys.argv)
