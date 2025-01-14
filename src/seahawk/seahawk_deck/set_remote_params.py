"""
set_remote_params.py

Abstracts requesting to set another node's parameters via a service call to class
'SetRemoteParams'. To import this class to a program on the deck use 
'from .set_remote_params import SetRemoteParams'

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
"""
# ROS client library
from rclpy.node import Node 

# Type hints
from typing import Any

# Parameters
from rcl_interfaces.srv import SetParameters
from rclpy.parameter import Parameter

class SetRemoteParams():
    """
    Abstracts requesting to set another node's parameters via a service call to a class. 
    """

    def __init__(self, this_node: Node, other_node_name: str):
        """
        Set up request to set another node's parameters via a service named '/other_node_name/set_parameters'
    
        Args:
            this_node: Node which makes the request to set another node's parameters. Client node
            other_node_name: Name of the node whose parameters should be set. Parameter node
        """
        # Create service name. Services to set parameters must be named as '/other_node_name/set_parameters'
        srv_name = "/" + other_node_name + "/set_parameters"

        # Set up client to remotely set parameters of another node using a service
        self.__cli = this_node.create_client(SetParameters, srv_name)

        # Try to connect to the service (wait one second between attempts)
        while not self.__cli.wait_for_service(timeout_sec=1.0):
            this_node.get_logger().info(f"{srv_name} service not available, waiting again...")
        
        # Create a set parameter request object
        self.__req = SetParameters.Request()

        # List to store parameters before sending them
        self.__param_list = []

    def update_params(self, param_name: str, param_value: Any):
        """
        Appends a single new parameter given its name and new value to the list of parameters to set

        Args: 
            param_name: Name of the parameter
            param_value: Value of the parameter (note must of a be a valid parameter type)
        """
        self.__param_list.append(Parameter(name=param_name, value=param_value).to_parameter_msg())
	
    def send_params(self) -> bool:
        """
        Sends updated parameter list to the service

        Returns:
            True if the parameters were correctly set, otherwise False
        """
        self.__req.parameters = self.__param_list   # Create updated param list
        future = self.__cli.call_async(self.__req)  # Send param to service
        self.__param_list.clear()                   # Reset list
        return future.result()                      # Return if the parameter is set correctly