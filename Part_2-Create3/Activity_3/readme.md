# Activity 3 - Actions with the physical buttons

In this activity we will first try sending goals to the Create3 from the terminal, then we will create a node that sends an action when one of the interface buttons on the Create3 is pressed.

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


## Conclusion

After completing this activity, you should be familiar with ...

## Navigation menu

- Go to [Part 2 - Create3](/Part_2-Create3/readme.md)
- Go to the [Main page](/readme.md)