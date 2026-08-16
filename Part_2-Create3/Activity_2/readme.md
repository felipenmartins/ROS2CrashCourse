# Activity 2 - IR sensors and Light Ring

This activity will focus on creating a node that activates the LEDs of the Light Ring of the Create3 robot depending on the readings from the front-facing proximity sensors. This is similar to what we saw in Activity 1 when running `ir_proximity_obstacles.py`, but now we are going to develop a ROS node for it.

## Step 1 - Connecting to the robot

To connect to the robot, your computer running ROS must be connected to the same WiFi network as the robot.

Turn the robot ON by placing it on the charging dock with the front sensor facing the dock's sensor. You should see the robot's light ring turn on when you do this. Wait for around 2-3 minutes while the robot boots up and connects to the wifi network. You should hear two "happy sounds" from your robot: one when it boots up and another one when it successfully connects to WiFi.

You can check if your robot is successfully connected to the same network as you by  opening a new terminal window listing the current topics using `ros2 topic list`. You should now see an output similar to:

```bash
/battery_state
  /cmd_audio
  /cmd_lightring
  /cmd_vel
  /dock
  /hazard_detection
  /imu
  /interface_buttons
  /ir_intensity
  /ir_opcode
  /kidnap_status
  /mouse
  /odom
  /parameter_events
  /robot_state/transition_event
  /rosout
  /slip_status
  /static_transform/transition_event
  /stop_status
  /system_monitor/transition_event
  /tf
  /tf_static
  /wheel_status
  /wheel_ticks
  /wheel_vels
```

If there are multiple robots in the same network, you will find that every node or topic your robot is running will be prepended by the robots name (i.e: `/robot_1/battery_state`). If you are at Hanze, you can find your robot identifier on the top faceplate of the robot and on its charging dock. For most of the commands in the workshop, you will need to prepend the commands with the correct robot name.

## Step 2 - Inspecting the topic of the proximity sensors

The Create3 publishes raw readings from its IR sensors on the topic `ir_intensity`. Let's start by seeing the data from this topic. As we learned before, we can echo the data from the topic by using the `ros2 topic echo <topic_name>` command.

Open a new terminal window and enter the following command, replacing robot-1 with your robot's name:

```bash
ros2 topic echo /robot_1/ir_intensity
```

You should see a similar output to the one below:

```bash
- header:
  stamp:
    sec: 1662590667
    nanosec: 512966282
  frame_id: base_link
readings:
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_side_left
  value: 0
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_left
  value: 2
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_front_left
  value: 4
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_front_center_left
  value: 7
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_front_center_right
  value: 9
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_front_right
  value: 10
- header:
    stamp:
      sec: 1662590667
      nanosec: 512966282
    frame_id: ir_intensity_right
  value: 0
---
```

As you can see, the message published contains the readings for each of the 7 proximity sensors. Try moving your hand in front of the bumper and see how the readings behave, this will be needed when you write your code later on. The result should be comparable to the one in Activity 1.

## Step 3 - Publishing to the Light Ring topic

The Create3 provides a topic where commands can be sent to control the robot's light ring. We are now going to send a test command to explore the message's format. Try sending following command in your terminal:

```bash
ros2 topic pub /robot_1/cmd_lightring irobot_create_msgs/msg/LightringLeds "{override_system: true, leds: [{red: 255, green: 0, blue: 0}, {red: 0, green: 255, blue: 0}, {red: 0, green: 0, blue: 255}, {red: 255, green: 255, blue: 0}, {red: 255, green: 0, blue: 255}, {red: 0, green: 255, blue: 255}]}"
```

This should make your robot's light ring colorful. 

As you can see, the message published on this topic is of type `irobot_create_msgs/msg/LightringLeds` and is relatively intuitive to use. Try playing around with the values and see them change yourselves.

To return the lightring to the default color, just send an empty message on the topic like so:

```bash
ros2 topic pub /robot_1/cmd_lightring irobot_create_msgs/msg/LightringLeds "{}"
```

## Step 4 - Understanding message structure

Before we can write code to use these topics, we must understand the structure of each message. This is a task you will have to do whenever you interact with a new topic or action, so it is important to understand this process well.

Using the `ros2 interface show <interface-name>` command we can investigate the structure of messages. Let's look at the message for the `ir_intensity` topic: first, we must find out its message type by getting information about the topic:

```bash
ros2 topic info /robot_1/ir_intensity
```

You should see a message similar to this:

```bash
Type: irobot_create_msgs/msg/IrIntensityVector
  Publisher count: 1
  Subscription count: 0
```

As you can see, the message type is `irobot_create_msgs/msg/IrIntensityVector`. Using this information, we can check the message structure (called _interface_ in ROS):

```bash
ros2 interface show irobot_create_msgs/msg/IrIntensityVector
```

As a result, you should be able to see the message structure. Note its fields and their hierarchy:

```bash
std_msgs/Header header
    builtin_interfaces/Time stamp
        int32 sec
        uint32 nanosec
    string frame_id
irobot_create_msgs/IrIntensity[] readings
    std_msgs/Header header
        builtin_interfaces/Time stamp
            int32 sec
            uint32 nanosec
        string frame_id
    int16 value
```

By inspecting the above result, you can see that the message consists of two top-level fields: `header` (of type `std_msgs/Header`) and `readings` (of type `irobot_create_msgs/IrIntensity[]`). Note a few things here:

- The hierarchy of the fields is described by their indentation (e.g: The `value` field is a part of the `readings` field )
- The `readings` field is an array, evidenced by the `[]`

## Step 5 - Create a node to print IR values

Now, let's see what this will look like in Python. Copy the simple subscriber code below in a new file and run it, making sure to change the topic name according to your namespace (if you need a reminder on how to do this, review steps 4-8 of Activity 1.2.1 from [part 1, chapter 1](/Part_1-ROS/Chapter-1/readme.md)).

```python
#!/usr/bin/env python3

from irobot_create_msgs.msg import IrIntensityVector
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from irobot_create_msgs.msg import IrIntensityVector
from rclpy.qos import ReliabilityPolicy, QoSProfile

class ir_subscriber(Node):

    def __init__(self):
        super().__init__("ir_subscriber")
        
        # Subscribe to the ir_intensity topic, which has a message with type IrIntensityVector
        self.irSubscriber = self.create_subscription(IrIntensityVector,"/robot_1/ir_intensity",self.ir_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        # Remember to change /robot_1 by to the namespace of your robot!

    def ir_callback(self,msg):
        print('Message type is:',type(msg))
        print('\n Header data is:', msg.header)
        print('\n The readings data is:',msg.readings)
   
def main():
    rclpy.init()
    subcriberNode = ir_subscriber()
    rclpy.spin_once(subcriberNode)

if __name__ == '__main__':
    main()
```

You should see it output a message similar to this:

```bash
Message type is: <class 'irobot_create_msgs.msg._ir_intensity_vector.IrIntensityVector'>

Header data is: std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='base_link')

The readings data is: [irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_side_left'), value=15), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_left'), value=415), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_left'), value=502), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_center_left'), value=32), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_center_right'), value=26), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_right'), value=366), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_right'), value=2897)]
```

As you can see, this reflects what we saw in the terminal earlier. In our case, `type(msg)` returns the message type, which is of the same type we saw in the terminal before. We can also access the `header` and `readings` variables simply by `msg.header`and `msg.readings`, much like the way we can access a normal Python dictionary.

> **Exercise:** Using that same logic, add instructions to the code to access and print the value of the first element of the `readings` array.

## Step 6 - Create nodes to control the light ring

Now, let's do the same for the `cmd_lightring` topic. Use the template below to create a node that turns the light ring completely blue.

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from irobot_create_msgs.msg import IrIntensityVector, LightringLeds, LedColor
from rclpy.qos import ReliabilityPolicy, QoSProfile

class lightController(Node):

    def __init__(self):
        super().__init__("lightController")
        
        #Publish to the cmd_lightring topic, which uses messages with type LightringLeds
        self.lightringPublisher  = self.create_publisher(LightringLeds,"cmd_lightring",10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        

    def timer_callback(self):
        #Initilaize message to correct message type
        msg = LightringLeds()
        msg.override_system = True #To override the default lightring settings
        
        #!Write your own code here!
        # Set all 6 LEDs to blue

        self.lightringPublisher.publish(msg)

        print("Publishing...")
      

def main():
    rclpy.init()
    controller = lightController()
    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```

Using the same concepts we used in the talker-listener nodes we created in Part 1, Chapter 1, and what we learned about the message type, we can create a simple node that subscribes to `ir_intensity` topic and publishes to the `cmd_lightring`. 

Use the template below to create a similar behavior to the one we observed in Activity 1 when we ran `ir_proximity_obstacles.py` (changing the color of the light ring depending on the values of the IR sensors). You can do whatever you want, like change it to red if the robot is close to any obstacle and green otherwise, or maybe assign a color to each sensor's readings.

```python
from rclpy.node import Node
from std_msgs.msg import String
from irobot_create_msgs.msg import IrIntensityVector, LightringLeds, LedColor
from rclpy.qos import ReliabilityPolicy, QoSProfile

class lightController(Node):

    def __init__(self):
        super().__init__("lightController")
        
        # Subscribe to the ir_intensity topic, which has a message with type IrIntensityVector
        self.irSubscriber = self.create_subscription(IrIntensityVector,"ir_intensity",self.ir_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        # Publish to the cmd_lightring topic, which uses messages with type LightringLeds
        self.lightringPublisher  = self.create_publisher(LightringLeds,"cmd_lightring",10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Define the ir_readings variable to store readings
        self.ir_readings = []


    def timer_callback(self):
        # Initilaize message to correct message type
        msg = LightringLeds()
        msg.override_system = True # To override the default lightring settings

        # Defining some LED colors to use later using the LedColor message type
        blueLed = LedColor(red=0, green=0, blue=255)
        redLed = LedColor(red=255, green=0, blue=0)
        greenLed = LedColor(red=0, green=255, blue=0)
        offLed = LedColor()

        # Main Logic
        if self.ir_readings: # Check if a valid reading exists
            #! Write your code here!
            # You can delete the example below and replace it with your logic.
            
            #! Example
            # If the left proximity sensor detects a close object    
            if self.ir_readings[0].value > 100: 
                # Make all 6 LEDs blue
                msg.leds = [blueLed, blueLed, blueLed, blueLed, blueLed, blueLed]
            
            
        self.lightringPublisher.publish(msg)

        print("Publishing...")
    
    def ir_callback(self,msg):
        self.ir_readings = msg.readings


def main():
    rclpy.init()
    controller = lightController()
    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```

> **Note that you will need to change the topic names to reflect your robot's name (e.g: `ir_intensity` => `robot-1/ir_intensity`)**

## Conclusion

After completing this activity, you should be familiar with creating nodes to interact with the IR sensors and Light Ring of the Create3 robot. In the next activity, we will study how to program the robot buttons to send ROS Actions goals.

## Navigation menu

- Continue to [Activity 3 - Actions with the physical buttons](../../Part_2-Create3/Activity_3/readme.md)
- Go to [Part 2 - Create3](../../Part_2-Create3/readme.md)
- Go to the [Main page](../../readme.md)