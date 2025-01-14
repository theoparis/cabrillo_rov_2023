'''
seahawk_rov/bno085.py

code for publishing the data from the bno085 sensor

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

# ros message
from sensor_msgs.msg import Imu

# import the bno085 circuit python sensor library
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C

from rclpy import executors
import rclpy


class BNO085:
    def __init__(
            self, 
            node, 
            i2c_bus,
            i2c_addr = 0x4a,
            frame_id = 'base_link',
            hardware_location = 'unknown'

        ):

        self.frame_id = frame_id
        self.node = node
        # instantiate the publisher
        self.publisher = node.create_publisher(Imu, hardware_location + '/' + 'imu', 10)

        # instantiate the sensor
        self.bno = BNO08X_I2C(i2c_bus=i2c_bus, address=i2c_addr)

        # enable raw data outputs
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION)

    def publish(self):
        # instantiate an imu message
        msg = Imu()

        # add the frame id
        msg.header.frame_id = self.frame_id

        # load the message with data from the sensor
        # IMU X right, Y forward, Z up
        # ROS Y left, X forward, Z up
        msg.orientation.x = self.bno.geomagnetic_quaternion[1]
        msg.orientation.y = -self.bno.geomagnetic_quaternion[0]
        msg.orientation.z = self.bno.geomagnetic_quaternion[2]
        msg.orientation.w = self.bno.geomagnetic_quaternion[3]
        msg.angular_velocity.x = self.bno.gyro[1]
        msg.angular_velocity.y = -self.bno.gyro[0]
        msg.angular_velocity.z = self.bno.gyro[2]
        msg.linear_acceleration.x = self.bno.linear_acceleration[1]
        msg.linear_acceleration.y = -self.bno.linear_acceleration[0]
        msg.linear_acceleration.z = self.bno.linear_acceleration[2]

        try:
            self.publisher.publish(msg)
        except executors.handler.exception():
            self.node.get_logger().info("Warning: IMU failed to publish")

def main(args=None):
    rclpy.init(args=args)
    test = BNO085()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
