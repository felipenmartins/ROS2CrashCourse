# Activity 1 - IR sensors and LED pannel
This activity will focus on creating a node that activates the LEDs on the Create3 robot depending on the readings from the front-facing proximity sensors.

### Task 1.0: Connecting to the robot
To connect to the robot, you must be connected to the same wifi network as the robot. Make sure you are connected to the `linksys` network first.
 
Then, place your robot on the charging dock with the front sensor facing the dock's sensor, you should see the robot's lightring turn on when you do this. Wait for around 2-3 minutes while the robot boots up and connects to the wifi network. You should hear two "happy" sounds from your robot, one when your robot boots up and another one when it successfully connects to wifi .
 
You can test to see if your robot is successfully connected to the same network as you by  opening a new terminal window listing the current topics using `ros2 topic list` command as before
 
You should now see an output similar to this 

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
    
Since there are multiple robots here, you will find that every node or topic your robot is running will be prepended by the robots name (i.e: `/robot_1/battery_state`). You can find your robot identifier on the top faceplate of the robot. For most of the commands in the workshop, you will need to prepend the commands with the correct robot name.

If you still do not see the topics being published by your robot after a few minutes have passed ,or if your lightring turns into a color other than white, please ask for assistance.
 
### Task 1.1: Inspecting the `ir_intensity` topic
The Create3 publishes the raw readings from the ir sensors on the `ir_intensity` topic. 
 
Let's start by seeing the data from this topic. As we learned before, we can echo the data from the topic by using the `ros2 topic echo <topic_name>` command.

Open a new terminal window and enter the following command,replacing robot-1 with your robot's number:

```bash
ros2 topic echo /robot_1/ir_intensity
```
    
You should now be able to see a similar output to the one below in your terminal window.

```   
      header:
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

As you can see, the message published contains the readings for each of the 7 proximity sensors in the front bumper.
 
Try moving your hand in front of the bumper and see how the readings behave, this will be needed when you write your code later on.
 
### Task 1.2: Publishing to the `cmd_lightring` topic
 
The Create3 provides a topic where commands can be sent to control the robot's lightring. We are now going to send a test command to test that and explore the message's format
 
Try sending following command in your terminal:

```bash
ros2 topic pub /robot_1/cmd_lightring irobot_create_msgs/msg/LightringLeds "{override_system: true, leds: [{red: 255, green: 0, blue: 0}, {red: 0, green: 255, blue: 0}, {red: 0, green: 0, blue: 255}, {red: 255, green: 255, blue: 0}, {red: 255, green: 0, blue: 255}, {red: 0, green: 255, blue: 255}]}"
```

This should turn your robot's lightring into a colorful ring of colors.
 
As you can see, the message published on this topic is of type `irobot_create_msgs/msg/LightringLeds` and is relatively intuitive to use. 
 
Try playing around with the values and see them change yourselves.
 
To return the lightring to the default color, just send an empty message on the topic like so:
 
```bash
ros2 topic pub /robot_1/cmd_lightring irobot_create_msgs/msg/LightringLeds "{}"
```  
### Task 1.3: Understanding message structure

Before we can write our code to use these topics, we must understand the structure of each message since we will need to create them ourselves later in our code. This is a task you will have to do whenever you interact with a new topic or action, so try and understand this process well.

#### Inspecting the `ir_intensity` topic
Using the `ros2 interface show <interface-name>` command we can see the exact structure of our messages. For example, let's look at the message for the `ir_intensity` topic. 

First, we can find out the message type using the `ros2 topic info <topic-name>` command:

```bash
ros2 topic info /robot_1/ir_intensity
```

You should see a message similar to this:
``` 
 	Type: irobot_create_msgs/msg/IrIntensityVector
    Publisher count: 1
    Subscription count: 0
```
   
As you can see above, the message type is `irobot_create_msgs/msg/IrIntensityVector`. Using this information, we can see the exact message structure like so:

```bash
ros2 interface show irobot_create_msgs/msg/IrIntensityVector
```

Now you should be able to see the message structure. Note the fields it contains and their hierarchy.

```
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
    
As you can see, the message consists of two top-level fields, a `header` field with type `std_msgs/Header` and a `readings` field with a type of `irobot_create_msgs/IrIntensity[]`. Note a few things here:

- The `readings` field is an array
- The hierarchy of the fields is described by their indentation (e.g: The `value` field is a part of the `readings` field )
    
Now, let's see what this will look like in Python. Copy the simple subscriber code below in a new file and run it, making sure to change the topic name according to your namespace.

```python
from irobot_create_msgs.msg import IrIntensityVector

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from irobot_create_msgs.msg import IrIntensityVector
from rclpy.qos import ReliabilityPolicy, QoSProfile

class ir_subscriber(Node):

    def __init__(self):
        super().__init__("ir_subscriber")
        
        #Subscribe to the ir_intensity topic, which has a message with type IrIntensityVector
        self.irSubscriber = self.create_subscription(IrIntensityVector,"/robot_1/ir_intensity",self.ir_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        

    def ir_callback(self,msg):
        print('Message type is:',type(msg))
        print('\n Header data is:', msg.header)
        print('\n The readings data is:',msg.readings)
        #! Write your code here!
        #Print the value of the first element in the readings array
   
def main():
    rclpy.init()

    subcriberNode = ir_subscriber()

    rclpy.spin_once(subcriberNode)

if __name__ == '__main__':
    main()
```
  
You should see it output a message similar to this:

``` 
     Message type is: <class 'irobot_create_msgs.msg._ir_intensity_vector.IrIntensityVector'>

     Header data is: std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='base_link')

     The readings data is: [irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_side_left'), value=15), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_left'), value=415), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_left'), value=502), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_center_left'), value=32), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_center_right'), value=26), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_front_right'), value=366), irobot_create_msgs.msg.IrIntensity(header=std_msgs.msg.Header(stamp=builtin_interfaces.msg.Time(sec=1664227973, nanosec=512763090), frame_id='ir_intensity_right'), value=2897)]
```

As you can see, this reflects what we saw in the terminal earlier. In our case, the `msg` variable contains the message type, which we can see is of the same type we saw in the terminal before. We can also access the `header` and `readings` variables simply by `msg.header`and `msg.readings`, much like the way we can access a normal Python dictionary. 
 
Using that same logic, try accessing the value of the first element of the `readings` array.
 
### Task 1.4: Creating a Node
Now, let's do the same for the `cmd_lightring` topic. Try creating a node that turns the lightring completely blue. To save some time, you can use the template below:

```python
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
        #Set all 6 LEDs to blue

        self.lightringPublisher.publish(msg)

        print("Publishing...")
      

def main():
    rclpy.init()

    controller = lightController()

    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```
 	
 
#### Writing the code
Using the same concepts we used in the talker-listener nodes we created before and what we learned about the message type, we can create a simple node that subscribes to `ir_intensity` topic and publishes to the `cmd_lightring` topic like so:

```python
from rclpy.node import Node
from std_msgs.msg import String
from irobot_create_msgs.msg import IrIntensityVector, LightringLeds, LedColor
from rclpy.qos import ReliabilityPolicy, QoSProfile

class lightController(Node):

    def __init__(self):
        super().__init__("lightController")
        
        #Subscribe to the ir_intensity topic, which has a message with type IrIntensityVector
        self.irSubscriber = self.create_subscription(IrIntensityVector,"ir_intensity",self.ir_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        #Publish to the cmd_lightring topic, which uses messages with type LightringLeds
        self.lightringPublisher  = self.create_publisher(LightringLeds,"cmd_lightring",10)
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        #Define the ir_readings variable to store readings
        self.ir_readings = []


    def timer_callback(self):
        #Initilaize message to correct message type
        msg = LightringLeds()
        msg.override_system = True #To override the default lightring settings

        #Defining some LED colors to use later using the LedColor message type
        blueLed = LedColor(red=0,green=0,blue=255)
        redLed = LedColor(red=255,green=0,blue=0)
        greenLed = LedColor(red=0,green=255,blue=0)
        offLed = LedColor()

        #Main Logic
        if self.ir_readings: #Check if a valid reading exists
			#! Write your code here!
            #You can delete the example below and replace it with your logic.
            
            #! Example
            #If the left proximity sensor detects an object    
            if self.ir_readings[0].value >100: 
            	#Make all 6 LEDs blue
                msg.leds = [blueLed,blueLed,blueLed,blueLed,blueLed,blueLed]
            
            
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
    
Explore how you can now use the data from `ir_intensity` topic to change the lightring's colors accordingly. You can do whatever you want, like change it to red if the robot is close to any obstacle and green otherwise or maybe assign a color to each sensor's readings. 

> **Note that you will need to change the topic names to reflect your robot's name (e.g: `ir_intensity` => `robot-1/ir_intensity`)**

