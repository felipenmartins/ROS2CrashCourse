# Chapter 3 - TFs, RViz and Gazebo

This chapter covers a few important concepts that will allow you to fully harness the power of ROS 2. You will be able to add packages to your existing workspace, learn how to use RViz and Gazebo for visualization and simulation, and understand the role of transforms (TFs) in ROS.

## Objectives

By the end of this chapter you should:

- Have a better understanding of ROS packages and how to add them to your workspace
- Know about simulation with Gazebo
- Know about visualizing sensor data with RViz
- Understand TFs and be able to visualize them in RViz

## 3.1 Packages

We dealt with packages in Chapter 1, when we created our own simple package with two nodes (a publisher and a subscriber). But a ROS package can contain much more than nodes, like ROS-independent libraries, datasets, configuration files, third-party software, or anything else that logically constitutes a useful module. If you want to be able to install your code or share it with others, then you’ll need it organized in a package. With packages, you can also use ROS 2 software developed by the ROS community. That's what we are going to do in this Chapter.

One of the biggest advantages of using ROS is its community and vast collection of packages. A lot of the most common use cases in robotics have official ROS packages created and supported by the team behind ROS, and for virtually any other use case, you can probably find a communty-created ROS package.

Often, you will need to install packages to interface sensors or external devices such as cameras, LiDARs or other sensors with your ROS-based robot. You might also need to install a ROS package that contains an algorithm that might help you in your project (e.g: sensor-fusion, localization, or mapping). For almost all of these cases, you will be able to find them on Github, but you will often need to check if they are compatible with your version of ROS.

Some commonly used ROS packages that you should at least know about are:

- [**Nav2**](http://nav2.org/) is the successor of the ROS Navigation Stack for mobile robot navigation. It provides easily-customizable methods for dynamic path planning, obstacle avoidance, behavior tree implementation etc.. It is used for all types of navigation applications, including drone navigation (see [Elroy Air](https://elroyair.com/)).

- [**MoveIt**](https://moveit.ai/) is a motion planning framework based on ROS. It is one of the most comprehensive and widely used ROS packages. It provides complete motion and grasp planning support for robotic manipulators of all types. It is widely used in a variety of fields and companies, like NASA, Google, Microsoft, and Samsung.

Later in this chapter we will practice how to add packages to our existing workspace.

## 3.2 Gazebo

[Gazebo](https://gazebosim.org/home) is an open-source 3D **robotics simulator** that is very commonly used to simulate robots using ROS. Gazebo uses the ODE physics engine, supports OpenGL rendering and has a vast community that provides plugins for simulating all kinds of sensors and actuators.

With Gazebo, you can create a fully virtual version of you robot, as well as all its sensors and actuators and test it in any virtual environment you need. For most commercially available robots, you will find that the company that created the robot usually provides all the files required to create that simulation, such as a 3D model of the robot, the robot's [URDF model](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html), and Gazebo plugins that can simulate all its sensors and actuators.

From the perspective of a robot programmer, Gazebo can be very useful as it's simulation publishes nearly identical topics to the ones the real robot does, which means we can test all our code in simulation before deploying to the live robot. You can create a world for your robot using Gazebo's world editor, or you can use one of the hundreds of community-created worlds. Figure 1 shows a screenshot of Gazebo running a simulation of the Create3 robot.

![Gazebo screenshot](/Part_1-ROS/Chapter-3/gazebo_screenshot.jpg)

##### Figure 1. Gazebo screenshot showing the simulation environment. You can control the robot by clicking the command buttons on the bottom right. 

More often than not, Gazebo is used to stress test the code before deploying, as it allows us to test any kind of algorithm freely without the risk of damaging the robot or any expensive equipment. It can also save incredible amounts of time as the simulation can be sped up to be many times faster than realtime, but the speed of the simulation largely depends on the machine running the simulation as it can often times be very resource intensive.

For more information about Gazebo, check its [getting started guide](https://gazebosim.org/docs/harmonic/getstarted/) and [Simulation Tutorials](https://gazebosim.org/docs/harmonic/tutorials/).

> Unfortunately, Gazebo is quite resource demanding and usually does not run well in virtual machines.

## 3.3 RViz

RViz is a **ROS Visualization** tool commonly used during software development. Unlike Gazebo, RViz is **not** a simulator, but a 3D visualization tool that can be used to visualize all kinds of robot data (real or simulated), from sensor data to actuators. It can be used together with Gazebo, but it does not output data on its own - it just shows existing data being published by other nodes. Figure 2 shows a screenshot of RViz with the Create3 robot.

![RViz screenshot](/Part_1-ROS/Chapter-3/rviz_screenshot.jpg)

##### Figure 2. RViz screenshot with the Create3 robot. The menu on the left side allows you to control what RViz shows, which can include sensor data, reference frames etc..

For details on how to use this tool, check out the [RViz User Guide]((https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)).

## 3.4 Activity: Adding Packages to the your workspace

This activity will focus on adding new packages to your workspace that will allow you to simulate the Create3 robot and visualize its data. We will need to clone some dependencies from Github and build the workspace again.

### Step 1 - Clone packages

Now we will clone a couple of packages from GitHub: the [Create3 simulation](https://github.com/iRobotEducation/create3_sim) and the [Create3 examples](https://github.com/iRobotEducation/create3_examples) packages. We will download them from their respective Github repositories.

Navigate to the `src` directory in your workspace and clone the packages from GitHub:

```bash
cd ~/create3_ws/src
```

Clone the iRobot® Create® 3 Simulator repository for ROS 2 Jazzy:

```bash
git clone https://github.com/iRobotEducation/create3_sim.git --branch jazzy
```

And the Create3 Examples for ROS 2 Jazzy:

```bash
git clone https://github.com/iRobotEducation/create3_examples.git --branch jazzy
```

### Step 2 - Install dependencies

Some ROS packages require other packages to work properly (we say that they _depend_ on other packages). The packages we just downloaded need a lot of other packages and other system-dependencies before they can be used. Downloading such dependencies manually would take a very long time and would be prone to error. `rosdep` is a command-line tool for installing dependencies related to ROS packages.

To install the dependencies for the packages installed, navigate to the top of your workspace and use the `rosdep install` command:

```bash
cd ~/create3_ws/
rosdep install --from-path src --ignore-src -yi
```

This will install all the required dependencies in the workspace. This process may take a while depending on how extensive the packages are and how fast your system and Internet connection are.

You should see many messages to inform you about the installation process while it is being executed. Wait until the installation finishes before moving to step 3. If everything works correctly, the final message should indicate that all required dependencies were installed successfully:

```bash
.
.
.
Setting up ros-jazzy-controller-manager-msgs (4.45.2-1noble.20260615.105226) ...
Setting up ros-jazzy-controller-manager (4.45.2-1noble.20260615.164916) ...
Setting up ros-jazzy-gz-ros2-control (1.2.19-1noble.20260615.171757) ...
#All required rosdeps installed successfully
```

### Step 3 - Build the workspace

Because we made changes to our workspace, we need to build it again. We will use the same build tool that we used in the activity of Chapter 1. Navigate to your main workspace directory and build it using the `colcon build` command:

```bash
cd ~/create3_ws
colcon build --symlink-install
```

This process usually takes a while, depending again on the speed of the system (it took more than 3 minutes in my machine). When the build process is complete you should see a message similar to this:

```bash
Summary: 16 packages finished [3min 28s]
```

### Step 4 - Update a package (if needed)

In some cases, the installed ROS packages might not be fully compatible with your ROS installation. If you are running the virtual machine provided by me, this is the case. In particular, `ros-jazzy-controller-manager` is newer than `ros-jazzy-diagnostic-updater`, which can be verified by running the command:

```bash
apt list --installed | grep diagnostic-updater
```

The expected result is:

```bash
ros-jazzy-diagnostic-updater 4.2.7
```

If your version is older than that, you should update the package:

```bash
sudo apt update
sudo apt install ros-jazzy-diagnostic-updater
```

After that, run the command above to list the installed packages again to verify that it now has the correct version.

### Step 5 - Source your workspace

Remember that you need to source your workspace every time you open a new terminal in order to run the packages installed in it:

```bash
cd ~/create3_ws
source install/local_setup.bash
```

### 6 - Test your installation

The packages we installed include files that allow simulating the Create3 in Gazebo and visualize it in RViz. We are going to discuss Gazebo and RViz in the next section. For now, you can test your installation by running the create3_gz launch file (which loads RViz, Gazebo and related nodes):

```bash
ros2 launch irobot_create_gz_bringup create3_gz.launch.py
```

During the launch process, you will see many log messages in the terminal and two new program windows. It might take a long while for all nodes to be loaded but, when everything is running, you should see a window with with RViz and another with Gazebo. If everything works as expected, RViz and Gazebo should look like the screenshots shown in Figures 1 and 2.

To close these windows, go back to the terminal where you launched them and press `CTRL + C`. **It is not recommended to close the windows manually as it might cause issues!**

After waiting for a few minutes for Gazebo to fully launch, open a new terminal window and run the `ros2 topic list` command to see the list of topics published by the Gazebo simulation node:

```bash
/battery_state
  /clicked_point
  /clock
  /cmd_audio
  /cmd_lightring
  /cmd_vel
  /diffdrive_controller/cmd_vel_unstamped
  /dock
  /dynamic_joint_states
  /goal_pose
  /hazard_detection
  /imu
  /initialpose
  /interface_buttons
  /ir_intensity
  /ir_opcode
  /joint_states
  /kidnap_status
  /mouse
  /odom
  /parameter_events
  /performance_metrics
  /robot_description
  /rosout
  /sim_ground_truth_dock_pose
  /sim_ground_truth_pose
  /slip_status
  /standard_dock_description
  /stop_status
  /tf
  /tf_static
  /wheel_status
  /wheel_ticks
  /wheel_vels
```

The topics being published are almost the same as the ones published by the real Create3 robot, which facilitates testing our code in simulation.

### Possible issues

If you are running ROS on a virtual machine, it is very possible that Gazebo will not run properly. Performance inside a VM may still be poor due to flickering, low frame rate, slow simulation, camera rendering issues etc.. Unfortunately, there's not much to do to fix this because Gazebo is quite demanding. If possible, use a machine with native Ubuntu 24.04 and ROS to run Gazebo.

RViz typically continues to work correctly even when Gazebo rendering is poor.

Another possible issue is that Gazebo opens but the simulation does not start. If RViz and Gazebo open, but then Gazebo crashes and the simulation never starts, it might be because it starts paused (that's what happened in my case, for hatever reason). You can verify that by running:

```bash
gz topic -e -t /world/depot/stats
```

If the output is `paused: true`, then you should unpause it as soon as Gazebo opens. To do that, prepare two terminal windows: one with the command to launch the simulation

```bash
ros2 launch irobot_create_gz_bringup create3_gz.launch.py
```

and another with the service call to unpause it:

```bash
gz service \
  -s /world/depot/control \
  --reqtype gz.msgs.WorldControl \
  --reptype gz.msgs.Boolean \
  --req 'pause: false'
```

First, run the ros2 launch command. As soon as Gazebo window opens, go to the other terminal and run the service call to unpause it. This should avoid Gazebo crashing.

## 3.5 TFs (Transforms) and Coordinate Frames

In all robotics applications, keeping track of various objects' locations in relation to one another and to their environment is essential. For example, a camera can locate the objects relative to its own coordinate frame, but this information is not useful to the robot unless it knows the transformation between the camera's base and its own coordinate frames.

In mobile robotics, the pose of all robot's sensors need to be defined with respect to the robot (by _pose_ we mean position _and_ orientation). By its turn, the pose of the robot needs to be referred to a fixed coordinate frame.

There are many possibilities to define reference frames (also called coordinate frames). In ROS, a common representation is shown in Figure 3, where:

- **map**: global reference frame to define the robot's coordinates on a 2D map.
- **odom**: robot's pose estimated via odometry - tracks the robot's movement from its starting point.
- **base_footprint**: 2D representation of the robot's footprint on the ground - typically used for path planning
- **base_link**: used as a reference for sensors and other components of the robot.
- **laser_link**: pose of a laser sensor on the robot - essential for interpreting its data for mapping and obstacle detection.

![Commonly used coordinate frames](https://wiki.ros.org/hector_slam/Tutorials/SettingUpForYourRobot?action=AttachFile&do=get&target=coordsystems_img.png)

##### Figure 3. Commonly used coordinate frames in mobile robotics. _Source: [ROS Wiki](https://wiki.ros.org/hector_slam/Tutorials/SettingUpForYourRobot)_

Often times, there will be at more than 5 different coordinate frames and maintaining the unique transformations to and from each one of these can be challenging, especially when they might change. ROS provides a package that optimizes this process:

**tf2** is a library to keep track of multiple coordinate frames over time. It publishes the relationship between coordinate frames (transforms) using a tree structure, allowing knowledge of the transformation between coordinate frames at any point in time. In other words, transforms (TFs) are used to describe the spatial relationships between different coordinate frames by providing the transformations (translations and rotations) between them. This is crucial for navigation, localization, mapping, sensor fusion, manipulation, and any other task executed by robots.

The relationship between these coordinate frames is determined with tf-tree. It essentially tells with a tree-like structure what is the child-frame's position in relation to the parent frame.

### 3.4.1 Activity: Visualizing TFs

We are now going to use TurtleSim to practice with coordinate frames and TFs. This activity is based on the one available in the [ROS documentation page](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html).

#### Step 1: Install dependencies

Before we start, we need to install the demo package and some dependencies by running the following command:

```bash
sudo apt-get install ros-jazzy-rviz2 ros-jazzy-turtle-tf2-py ros-jazzy-tf2-ros ros-jazzy-tf2-tools ros-jazzy-turtlesim
```

#### Step 2: Run the TurtleSim tf2 Demo

Now, run the command below to open TurtleSim:

```bash
ros2 launch turtle_tf2_py turtle_tf2_demo.launch.py
```

You will see two turtles: one that starts in the center (turtle1), and another that starts at the bottom of the screen (turtle2). Turtle2 moves towards Turtle1.

Open another terminal and run the teleop node:

```bash
ros2 run turtlesim turtle_teleop_key
```

Now you can control turtle1 using the keyboard keys. Move it around and see how the turtle2 runs after it.

How is this implemented?

The tf2 library is being used to create three coordinate frames: a world frame, a turtle1 frame, and a turtle2 frame. A tf2 broadcaster is used to publish the turtle coordinate frames, while a tf2 listener is used to calculate the difference between the two turtle frames. Turtle2 is moved to minimize that difference.

#### Step 3: Visualize the TF tree

By using `view_frames` we can see a diagram of the three frames being broadcast by tf2. It generates a PDF file with the tree diagram:

```bash
ros2 run tf2_tools view_frames
```

Wait a few seconds until the process is completed. Then, open the Ubuntu _Document Viewer_ application and open the PDF file that was saved by `view_frames`. You will see something similar to Figure 4. Notice that `world` is the parent frame of both `turtle1` and `turtle2`.

![TF2 tree](/Part_1-ROS/Chapter-3/tf2_tree.png)

##### Figure 4. The three coordinate frames that are broadcast by tf2: world (parent), turtle1, and turtle2. Some diagnostic information is also informed, like when the oldest and most recent frame transforms were received and how fast the tf2 frame is published.




---------------- Here --------------------



An easy and quick way to see your tf tree from the command line is to use the tools provided by the `tf2` package.

Install the `tf2` package with the following:

	sudo apt-get install ros-galactic-turtle-tf2-py ros-galactic-tf2-tools 	ros-galactic-tf-transformations
    
 Then, run the following command to collect a snapshot of your tf data and save it to a pdf:
 	
    ros2 run tf2_tools view_frames
    
Finally, view your tf tree:

	evince frames.pdf
    
 You should now see an image similar to this:
 
 ![Screenshot from 2022-09-30 00-19-42](https://user-images.githubusercontent.com/71664900/193152322-9e61b472-159d-49a1-906b-5905c6cdee9a.png)

 Scroll through the pdf to see all the different frames that make up the Create3. Next, we will see where they are exactly on the robot with RViz!
 
 #### Task 2: Now with RViz!
 In this activity, we will use RViz to visualize a the transforms published by the Create3.
 
 Open two new terminal windows, making sure to source your `ros2_ws`, and launch the following launch files:

```bash 
ros2 launch irobot_create_common_bringup rviz2.launch.py
```


```bash
ros2 launch irobot_create_common_bringup robot_description.launch.py
```
You should now see an RViz window open that looks similar to this:

![Screenshot from 2022-09-30 00-03-36](https://user-images.githubusercontent.com/71664900/193150412-f522ef0c-5c64-4dc9-a56b-1500eb48a018.png)


To see the Create3's frames visualized in RViz, you can click on the checkbox next to the "TF" option. Take a minute to play around with the options and see where each coordinate frame lies on the robot.

![Screenshot from 2022-09-30 00-22-16](https://user-images.githubusercontent.com/71664900/193152601-476d9fec-1583-48c3-8873-d80d8fd752e9.png)
 As you can see, the number of frames can be quite visually overwhelming. Try disabling a few of the frames from by unchecking a few of the checkboxes under the 'frames' menu

 ## 3.4 Launch Files
 Launch files are one of ROS' most useful features. Launch files allow us to run multiple nodes at once, and even what arguments to pass them on startup. This allows us to launch a complete application with whatever configuration we need from a single file.
 
 Launch files in ROS2 can be written in Python, XML, or YAML.
 
 
 ### 3.4.1: Activity - Working with Launch Files
 
 In this activity, we will go back our good friend turtlesim to see an example of how launch files work. We will be creating a simple launch file that launches the turtlesim node as well as the teleop node at the same time.
 
 This activity can also be found on the ROS2 docs [here.](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
 
 
 #### Tasks
 
 #### 0 - Setup
 
 Most of the time, you will find launch files stored inside a `launch` directory inside each package's directory. 
 
 For our case, we will just create it inside our `src` directory.
 
 	cd ~/ros2_ws/src
    mkdir launch
    cd launch
 
 Then, we can create our launch file like so:
 	
   	touch turtlesim_teleop_launch.xml
    
 We will also need to install the `xterm` package for this exercise, so install it now as well:
 	
    sudo apt install xterm
#### 1 - Write the launch file!


  We are going to create a simple launch file that launches both the `turtlesim_node` and the `turtle_teleop_key` executables from the `turtlesim` package

Copy and paste the code below into your launch files:

```xml
<launch>
  <node pkg="turtlesim" exec="turtle_teleop_key" output="screen" launch-prefix="xterm -e"/>
  <node pkg="turtlesim" exec="turtlesim_node"/>
</launch>
```

As you can see, the syntax for launch files is relatively intuitive. You can find out a lot more of what launch files are capable of by following the [ros2 tutorials here](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Launch-Main.html)

#### 2- Launch!

If you recall, the syntax for using launch files looks something like this:

	ros2 launch <package_name> <launch_file_name>
    
 But in our case, since this launch file is not part of a package, we can launch it directly like so:
  
  	cd ~/ros2_ws/src/launch
    ros2 launch turtlesim_teleop_launch.xml
    
 You should now be able to see two windows, one for the teleop node, and one for the turtlesim node:
 
 ![Screenshot from 2022-09-30 10-37-17](https://user-images.githubusercontent.com/71664900/193229137-f8a475d2-76ee-481a-8b7d-f22364c88806.png)
 ---

### 3.5 -  Rosbags

As you might have noticed, data sent over topics is not inherently persistent. If a message is not captured by a node, there is no way for it to be replayed back or stored. Although this behaviour is useful in many ways, sometimes data persistence is necessary. For example, when optimizing or testing algorithms, it can be very useful to capture data once during a data collection phase, and using that data later for optimizing algorithms or as training data

Fortunately, ROS provides a utility that allows for easy data persistence!

The `rosbag` utility allows you to store and replay topic data through the CLI commands.

You can find out all about the package again through the  [ros2 tutorials here](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html).

### 3.5.1 - A `rosbag` demo

In this very short demo, we will try recording a few topics in turtlesim using the `rosbag2` package and replay them back in real time

This activity can be found on the ROS2 wiki [here](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html)

#### Task 0 - Setup

Download the `rosbags2` package like so:
	
    sudo apt-get install ros-galactic-ros2bag \ros-galactic-rosbag2-storage-default-plugins
    
Then create a directory for your rosbag files to go

	mkdir ~/rosbag_demo
    cd ~/rosbag_demo
    
Now, run the turtlesim and turtle_teleop nodes

```bash 
ros2 run turtlesim turtlesim_node 
```
```bash 
ros2 run turtlesim turtle_teleop_key 
```    
    
#### Task 1 - Record a topic

In our example, we will record the `/turtle1/cmd_vel` topic, which contains all the velocity commands for turtlesim

To record a topic, we can use the following syntax

	ros2 bag record <topic_name>
    
 or to record multiple topics:
 
 	ros2 bag record <topic1_name> <topic2_name> 

You can also add a custom name using the `-o` flag like so:

	ros2 bag record -o <file_name> <topic_name>
    
 In our case, we will record the `/turtle1/cmd_vel` like so:
 
      ros2 bag record -o turtle_movement /turtle1/cmd_vel
    
  You should now see a similar screen:
  
  ```bash
  [INFO] [1664530714.080295473] [rosbag2_storage]: Opened database 'rosbag2_2022_09_30-11_38_34/rosbag2_2022_09_30-11_38_34_0.db3' for READ_WRITE.
[INFO] [1664530714.080414474] [rosbag2_recorder]: Listening for topics...
[WARN] [1664530714.081898406] [rosbag2_transport]: Hidden topics are not recorded. Enable them with --include-hidden-topics
[INFO] [1664530714.083271733] [rosbag2_recorder]: Subscribed to topic '/turtle1/cmd_vel'
[INFO] [1664530714.083715109] [rosbag2_recorder]: All requested topics are subscribed. Stopping discovery...
```
Now, switch to your teleop terminal, and move the turtle in a pattern that you can recognize later. When you are done, press `CTRL+C` to end the recording.


#### Task 2 - Inspect the rosbag

You can find out information about the exact data stored inside the rosbag by using the command `rosbag info <bag_name>`

To inspect the rosbag we just recorded:
	
    ros2 bag info turtle_movement

You should see something similar to this
```bash
Files:             turtle_movement_0.db3
Bag size:          16.8 KiB
Storage id:        sqlite3
Duration:          3.697s
Start:             Sep 30 2022 11:44:08.242 (1664531048.242)
End:               Sep 30 2022 11:44:11.940 (1664531051.940)
Messages:          28
Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 28 | Serialization Format: cdr

```
This shows you information about the exact topics recorded, their message types, the duration of the recording as well as some metadata about the bag itself like its size.

#### Task 3 - Replay the files!

Now we can replay our recorded topic data by simply running the following command:

	ros2 bag play turtle_movement
    
 If you have the turltesim window still open, you should now be seeing that your turtle repeat the same pattern you played before!
 
 These same concepts can of course be applied to any ros topic. Common use cases include collecting sensor data for training, optimizing, or testing sensor fusion algorithms.
 
 ## Navigation menu
- Continue to [Part 2 - Create3](/Part_2-Create3/readme.md)
- Go back to [Part 1 - ROS](/Part_1-ROS/readme.md)
- Go to the [Main page](/readme.md)
