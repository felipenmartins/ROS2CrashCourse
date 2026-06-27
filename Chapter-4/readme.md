# Working with the iRobot Create3

The purpose of this chapter is to practice some of the ROS 2 concepts on a real robot. The examples below assume you have access to an [iRobot Create3](https://iroboteducation.github.io/create3_docs/).

## The iRobot Create3 
 
The Create3 is an educational robot made by iRobot, who you may know as the company that created the Roomba vacuum cleaner. 

We will be using the Create3 robot to demonstrate the concepts we learn, so it is a good idea to get familiar with the robot.

Here are a few things you should know about the Create3:

### Overview

The Create® 3 is based on the Roomba®, a robot vacuum cleaner. Its sensors, actuators, and compact design are capable of navigating and mapping a the whole floor of a home or office space. 

![Create3](https://iroboteducation.github.io/create3_docs/hw/data/front_iso.jpg)

The front of the robot features a bumper with seven pairs of IR proximity sensors, which can be used to detect obstacles. The top of the robot contains three buttons which can all be overridden by a ROS 2 application. The power button features a ring of six RGB LEDs for indication.


![Create3](https://iroboteducation.github.io/create3_docs/hw/data/bottom.jpg)

The bottom of the robot includes four cliff sensors to keep the robot on solid ground, a front caster wheel, charging contacts, two wheels with current sensors and encoders, and an optical odometry sensor. The create3 also includes an onboard IMU, which is used with the optical odometry sensor and wheel encoders to generate a fused odometry estimate.

This section is an excerpt from the [create3 docs](https://iroboteducation.github.io/create3_docs/hw/overview/), head over there if you want to find out more about the robot

### Lightring and Buttons

The lightring and buttons on the top of the robot are the primary way you can interact with the robot. You can find what the buttons do as well as what all the different light ring patterns mean in [this guide here](https://iroboteducation.github.io/create3_docs/hw/face/) 
 
Now, onto the activity.

---

## Activity 1 - IR sensors and LED pannel
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


---

## Activity 2 - Actions with the physical buttons
In the next activity we will first try sending goals to the Create3 from the terminal, then we will create a node that sends an action when one of the interface buttons on the Create3 is pressed.

The Create3 has a few actions already created. You can check out all the actions [here](https://iroboteducation.github.io/create3_docs/api/ros2/) or by using the `ros2 action list` command when connected to the robot.

 ### Task 2.0 - Setup
 
 Just like before, we will turn on and connect to the Create3. If you forgot how to do that, refer to [this activity]().
 
 ### Task 2.1 - Send an `led_animation` action
 One of the actions that the Create3 provides is the `led_animation` action, which allows us to create animations for the robot's lightring. 
 
#### Inspecting the action
Using the commands we learned before, we can find out exactly how this command should look like. We can use the following command to find out the type of the `led_animation` action like so:

```bash
ros2 action list -t
```

This should return a list of all the currently available actions and their types:
 
```
    /audio_note_sequence [irobot_create_msgs/action/AudioNoteSequence]
    /dock [irobot_create_msgs/action/DockServo]
    /drive_arc [irobot_create_msgs/action/DriveArc]
    /drive_distance [irobot_create_msgs/action/DriveDistance]
    /led_animation [irobot_create_msgs/action/LedAnimation]
    /navigate_to_position [irobot_create_msgs/action/NavigateToPosition]
    /rotate_angle [irobot_create_msgs/action/RotateAngle]
    /undock [irobot_create_msgs/action/Undock]
    /wall_follow [irobot_create_msgs/action/WallFollow]
``` 

For now let's focus on the`/led_animation` action, which we can now see has a type of `irobot_create_msgs/action/LedAnimation`, which is a custom action type provided by the Create3.

```
    /led_animation [irobot_create_msgs/action/LedAnimation]
```

We can now use the `ros2 interface show <action_type>` command to find the exact structure of the `irobot_create_msgs/action/LedAnimation` like so:

```bash
ros2 interface show irobot_create_msgs/action/LedAnimation
```

You should now see the following output:
```
    # Request
    # Supported Animation types
    int8 BLINK_LIGHTS = 1
    int8 SPIN_LIGHTS = 2

    # Animation to apply
    int8 animation_type
    # LED values to apply to animation
    irobot_create_msgs/LightringLeds lightring
    # Time to apply animation
    builtin_interfaces/Duration max_runtime
    ---
    # Result
    builtin_interfaces/Duration runtime
    ---
    # Feedback
    # Time the animation has left to run
```

As you can see, we need to send the type of animation (blink/spin), a `LightringLeds` message like the one we used when previously controlling the lightring, and the duration for the animation. 

The action's result will simply be the duration it was active for, and its feedback will be the time it has left to run

We can now test out the action by sending the following command from the terminal, note the `--feedback` at the end which prints the action's feedback to the terminal

```
    ros2 action send_goal /robot-1/led_animation irobot_create_msgs/action/LedAnimation "{animation_type: 0, lightring: {leds: [{red: 255, green: 0, blue: 0}, {red: 0, green: 255, blue: 0}, {red: 0, green: 0, blue: 255}, {red: 255, green: 255, blue: 0}, {red: 255, green: 0, blue: 255}, {red: 0, green: 255, blue: 255}], override_system: true},max_runtime: {sec: 500, nanosec: 0}}" --feedback
```

### Task 2.2 - Action using Python
Now, let's see what that looks like with Python!

Using the concepts we learned before, send an `LedAnimation` action that makes the lightring blink blue for 5 seconds.

Like before, you can copy the boilerplate code below and fill the code under the `#!Write your code here!` marker. 

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from irobot_create_msgs.msg import LightringLeds, LedColor
from irobot_create_msgs.action import LedAnimation

class animationController(Node):

    def __init__(self):
        super().__init__("animationController")
        
        #Create an action client that sends an action of type LedAnimation to the action server led_animation
        self.action_client = ActionClient(self, LedAnimation, '/robot_1/led_animation')


    def send_goal(self):
    	#Initialize an empty LedAnimation action tyoe
        animationGoal = LedAnimation.Goal()
        
        #!Write your code here!

        ##Set Animation Type (1 for blinking, 2 for spinning)
        
        ## Set Runtime for the animation
		
        ##Create an empty lightring message
        
        ##Set the lightring colors
        
        
        #Wait for an action server to become available
        self.action_client.wait_for_server()
        
        print("Publishing Goal!")

        #Send the goal
        return self.action_client.send_goal_async(animationGoal)
    
        

def main():
    rclpy.init()

    controller = animationController()
    controller.send_goal()

    rclpy.spin(controller)

if __name__ == '__main__':
    main()

```

#### Inspecting the `/interface_buttons` topic

To use the buttons in our code, we need to be able to read the data from the `interface_buttons` topic.

Before echoing out the data from the topic, let's first explore its message type. We can find its message type using the `ros2 topic info` command like so:

```bash
ros2 topic info /robot_1/interface_buttons
```

Which should return an output that looks like this:
```
    Type: irobot_create_msgs/msg/InterfaceButtons
    Publisher count: 1
    Subscription count: 1
```
Let's echo the data from the topic like so:
```bash
	ros2 topic echo /robot_1/interface_buttons
```
You should see an output that looks something like this:
```
      ---
      header:
        stamp:
          sec: 1662634177
          nanosec: 64907707
        frame_id: base_link
      button_1:
        header:
          stamp:
            sec: 1662634177
            nanosec: 64907707
          frame_id: button_1
        is_pressed: false
        last_start_pressed_time:
          sec: 0
          nanosec: 0
        last_pressed_duration:
          sec: 0
          nanosec: 0
      button_power:
        header:
          stamp:
            sec: 1662634177
            nanosec: 64907707
          frame_id: button_power
        is_pressed: false
        last_start_pressed_time:
          sec: 0
          nanosec: 0
        last_pressed_duration:
          sec: 0
          nanosec: 0
      button_2:
        header:
          stamp:
            sec: 1662634177
            nanosec: 64907707
          frame_id: button_2
        is_pressed: false
        last_start_pressed_time:
          sec: 1662634169
          nanosec: 215865398
        last_pressed_duration:
          sec: 0
          naosec: 640038759
      ---
```
As you can see, the topic provides us with the pressed state of all the interface buttons, the time they were last pressed, as well as the duration they were pressed for. This information can allow us to create logic for various types of button presses (e.g Hold vs Press) and even multi-button actions.

For our case, we will simply be checking the `is_pressed` state to check if the button is currently pressed. Try pressing different buttons and see how the message changes accordingly.
 
 Before moving on to creating the code, try using the `ros2 interface show <interface_type>` to find out the exact structure of the message being sent on this topic.
 
#### Write the node!
 
It's now time to write the code that will make it all happen. Our node should create an LED animation action that's activated when button1 is pressed. 
 
You can also add whatever logic you want to the code. Try for example creating different animations for different button presses, or changing the animation's color on each subsequent button press.
 
Using the same concepts and code snippets we created before, we can create the following code:
 
 ```python
 import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from irobot_create_msgs.msg import InterfaceButtons, LightringLeds, LedColor
from irobot_create_msgs.action import LedAnimation
from rclpy.qos import ReliabilityPolicy, QoSProfile

class animationController(Node):

    def __init__(self):
        super().__init__("animationController")
        
        #Subscribe to the interface_buttons topic
        self.buttonSubscriber = self.create_subscription(InterfaceButtons,"interface_buttons",self.button_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        #Create an action client that sends an action of type LedAnimation to the action server led_animation
        self.action_client = ActionClient(self, LedAnimation, 'led_animation')


    def send_goal(self):
    	#Initialize an empty LedAnimation action tyoe
        animationGoal = LedAnimation.Goal()
        
        #Animation Type (1 for blinking, 2 for spinning)
        animationGoal.animation_type = 1
        
        #Runtime for the animation
        animationGoal.max_runtime.sec = 10
		
        #Initialize the lightring message
        animationGoal.lightring = LightringLeds()
        animationGoal.lightring.override_system = True

        #Defining some LED colors to use later using the LedColor message type
        blueLed = LedColor(red=0,green=0,blue=255)
        redLed = LedColor(red=255,green=0,blue=0)
        greenLed = LedColor(red=0,green=255,blue=0)
        offLed = LedColor()
        
        #Setting the lightring colors
        animationGoal.lightring.leds = [blueLed,blueLed,blueLed,blueLed,blueLed,blueLed]        
		
        #Wait for an action server to become available
        self.action_client.wait_for_server()
        
        #Send the goal
        return self.action_client.send_goal_async(animationGoal)

    
    def button_callback(self,msg):
        #! Write your code here!
        #Hint: To check if a button is pressed, use the is_pressed property 
        #Hint: To send a goal use the send_goal method created above
        
        
def main():
    rclpy.init()

    controller = animationController()

    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```

> **Note that you will need to change the topic and action names to reflect your robot's name (e.g: `interface_buttons` => `robot_1/interface_buttons`)**
 
#### Test your code!
Just like before, to run your code, navigate to the `scripts` folder and run the your python script like before:
 
```bash
cd ~create3_ws/src/scripts
python3 create3ButtonLight.py
```

Now try pressing the buttons on your robot and see your code in action!