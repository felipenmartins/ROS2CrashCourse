#!/usr/bin/env python3

# Import Libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Define the talker class based on the Node class from rclpy library
class talker(Node):
  # Constructor Method
  def __init__(self):
    # Create a node with name "talkerNode"
    super().__init__("talkerNode")
    # Create a publisher to the "myTopic" topic
    self.publisher = self.create_publisher(String, "myTopic", 10)
    
    # Define a timer_period variable
    timer_period = 0.5  # seconds
    # Create a timer to call the function timer_callback every timer_period
    self.timer = self.create_timer(timer_period, self.timer_callback)

  # Timer callback method
  def timer_callback(self):
    # Initialize empty message of type String
    msg = String()
    # Add data to the message
    msg.data = "Marco!"
    
    # Publish the message
    self.publisher.publish(msg)
    print("Publishing...")

# Main Function
def main():
  # Initialize rclpy
  rclpy.init()
  # Instantiate the talker class
  publisherNode = talker()
  # Spin Node(s)
  rclpy.spin(publisherNode)

# Call the main() function
if __name__ == '__main__':
  main()