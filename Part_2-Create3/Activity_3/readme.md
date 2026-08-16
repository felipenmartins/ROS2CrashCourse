# Activity 3 - Actions with the physical buttons

In this activity we will practice Action goals with the Create3. First, we will send goals via the terminal. Afterwards, we will create a node that sends an action goal when one of the interface buttons on the Create3 is pressed.

## Step 1 - Inspect available actions

Connect to the robot and get a list of all available actions via the command:

```bash
ros2 action list
```

> If you forgot how to turn on and connect to the Create3, please review [Activity 1](../../Part_2-Create3/Activity_1/readme.md)) and [Activity 2](../../Part_2-Create3/Activity_2/readme.md).

The Create3 has a few actions available. See more information [here](https://iroboteducation.github.io/create3_docs/api/ros2/).

One of the actions that the Create3 provides is the `led_animation`, which allows us to create animations for the robot's lightring. Let's find out the type of the `led_animation` action:

```bash
ros2 action list -t
```

This should return a list of all the currently available actions and their types:

```bash
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

## Step 2 - Call the LED animation action

For now let's focus on the`/led_animation` action, which has a type of `irobot_create_msgs/action/LedAnimation`. We can now use the `ros2 interface show <action_type>` command to find the exact structure of the action type:

```bash
ros2 interface show irobot_create_msgs/action/LedAnimation
```

You should now see the following output:
```bash
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

To call this action, we need to send the type of animation (blink/spin), a `LightringLeds` message like the one we used when previously controlling the lightring, and the duration for the animation. The action's result will simply be the duration it was active for, and its feedback will be the time it has left to run.

We can now test out the action by sending the following command from the terminal (note the `--feedback` at the end which prints the action's feedback to the terminal):

```
ros2 action send_goal /robot-1/led_animation irobot_create_msgs/action/LedAnimation "{animation_type: 0, lightring: {leds: [{red: 255, green: 0, blue: 0}, {red: 0, green: 255, blue: 0}, {red: 0, green: 0, blue: 255}, {red: 255, green: 255, blue: 0}, {red: 255, green: 0, blue: 255}, {red: 0, green: 255, blue: 255}], override_system: true},max_runtime: {sec: 500, nanosec: 0}}" --feedback
```

Observe the result and action feedback. Change the parameters of the command to get an idea of the pre-programmed LED animations.

## Step 3 - Use Actions in Python

Now, let's see how to do it with Python!

Using the concepts we learned before, let's create a node to send an `LedAnimation` action that makes the lightring blink blue for 5 seconds.

Like before, your task is to investigate what you need to write down to complete the template code below by filling out the part `#!Write your code here!` (if you need a reminder on how to do this, review steps 4-8 of Activity 1.2.1 from [part 1, chapter 1](../../Part_1-ROS/Chapter-1#121-activity-creating-your-own-workspace)):

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from irobot_create_msgs.msg import LightringLeds, LedColor
from irobot_create_msgs.action import LedAnimation

class animationController(Node):

    def __init__(self):
        super().__init__("animationController")
        
        # Create an action client that sends an action of type LedAnimation to the action server led_animation
        self.action_client = ActionClient(self, LedAnimation, '/robot_1/led_animation')


    def send_goal(self):
        # Initialize an empty LedAnimation action tyoe
        animationGoal = LedAnimation.Goal()
        
        #!Write your code here!
        ## Set Animation Type (1 for blinking, 2 for spinning)
        ## Set Runtime for the animation
        ## Create an empty lightring message
        ## Set the lightring colors
        
        # Wait for an action server to become available
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

## Step 4 - Investigate the buttons topic

Suppose you want to select the lightring color by clicking the Create3 buttons. We will change our code to impolemnent that, but first let's investigate the buttons topic to understand how it is organized. For that, let's first explore the message type of the topic `/interface_buttons`:

```bash
ros2 topic info /robot_1/interface_buttons
```

Which should return an output that looks like this:

```bash
Type: irobot_create_msgs/msg/InterfaceButtons
Publisher count: 1
Subscription count: 1
```

Let's echo the data from the topic to see how it looks like:

```bash
	ros2 topic echo /robot_1/interface_buttons
```

Click the buttons while the topic is being echoed to see the result. You should see an output that looks something like this:

```bash
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

As you can see, the topic provides us with the pressed state of the three interface buttons, the time they were last pressed, as well as the duration they were pressed for. This information allows us to create logic for various types of button presses (like press and hold) and even multi-button actions.

For our case, we will simply check the `is_pressed` state to verify that the button is currently pressed. Try pressing different buttons and see how the message changes accordingly.

Before moving on to creating the code, try using the `ros2 interface show <interface_type>` to find out the exact structure of the message being sent on this topic.

## Step 5 - Add button check to the code

Our node should create an LED animation action that's activated when button1 is pressed. Using the same concepts and code snippets we created before, complete the following code to complete this step:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from irobot_create_msgs.msg import InterfaceButtons, LightringLeds, LedColor
from irobot_create_msgs.action import LedAnimation
from rclpy.qos import ReliabilityPolicy, QoSProfile

class animationController(Node):

    def __init__(self):
        super().__init__("animationController")
        
        # Subscribe to the interface_buttons topic
        self.buttonSubscriber = self.create_subscription(InterfaceButtons,"interface_buttons",self.button_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))

        # Create an action client that sends an action of type LedAnimation to the action server led_animation
        self.action_client = ActionClient(self, LedAnimation, 'led_animation')


    def send_goal(self):
    	  # Initialize an empty LedAnimation action tyoe
        animationGoal = LedAnimation.Goal()
        
        # Animation Type (1 for blinking, 2 for spinning)
        animationGoal.animation_type = 1
        
        # Runtime for the animation
        animationGoal.max_runtime.sec = 10
		
        # Initialize the lightring message
        animationGoal.lightring = LightringLeds()
        animationGoal.lightring.override_system = True

        # Defining some LED colors to use later using the LedColor message type
        blueLed = LedColor(red=0,green=0,blue=255)
        redLed = LedColor(red=255,green=0,blue=0)
        greenLed = LedColor(red=0,green=255,blue=0)
        offLed = LedColor()
        
        # Setting the lightring colors
        animationGoal.lightring.leds = [blueLed, blueLed, blueLed, blueLed, blueLed, blueLed]        
		
        # Wait for an action server to become available
        self.action_client.wait_for_server()
        
        # Send the goal
        return self.action_client.send_goal_async(animationGoal)

    
    def button_callback(self,msg):
        #! Write your code here!
        # Hint: To check if a button is pressed, use the is_pressed property 
        # Hint: To send a goal use the send_goal method created above
        
        
def main():
    rclpy.init()
    controller = animationController()
    rclpy.spin(controller)

if __name__ == '__main__':
    main()
```

> **Note that you will need to change the topic and action names to reflect your robot's name (e.g: `interface_buttons` => `robot_1/interface_buttons`)**

You can also add whatever logic you want to the code. Try, for example, creating different animations for different button presses, or changing the animation's color on each subsequent button press.

Now run your code, try pressing the buttons on your robot, and the light ring reacting to it!

## Conclusion

After completing this activity, you should be familiar with the Create3 Actions and know how to write Python code to call them. As an exercise, modify your node to include calls to other actions of your choice.

## Navigation menu

- Go to [Part 2 - Create3](../../Part_2-Create3/readme.md)
- Go to the [Main page](../../readme.md)