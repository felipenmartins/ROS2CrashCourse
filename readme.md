# ROS 2 Crash Course

Welcome to the ROS 2 Crash Course!

This course covers fundamental ROS 2 concepts to equip you with the knowledge to run and create your own ROS 2-enabled software for robots. 

Examples are provided for the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot, but you can follow this course to learn ROS even if you do not have a physical robot. 

The course is organized in 3 chapters that cover ROS 2 and its core concepts, and one extra chapter dedicated to the Create3 robot: 

- [**Chapter 1: What is ROS?**](/Chapter-1/readme.md)
  - The history of ROS
  - Why use ROS?
  - Overview of ROS
  - Summary of CLI commands
- [**Chapter 2: Working with ROS**](/Chapter-2/readme.md)
  - TurtleSim
  - The ROS Graph
  - Nodes, Messages, Topics
  - Writting a node in Python
  - ROS Actions 
- [**Chapter 3: The ROS Ecosystem**](/Chapter-3/readme.md) 
  - ROS Packages
  - Workspaces
  - Simulation
  - RViz and TFs
  - Launch files
  - Bags
- [**Chapter 4: Working with the iRobot Create3**](/Chapter-4/readme.md)
  - Overview of the Create3
  - Activity 1 - IR sensors and LED pannel
  - Activity 2 - Actions with the physical buttons   


### Intended Learning Outcomes:
By the end of this course, you should be able to: 
- Understand fundamental concepts of ROS 2
- Run ROS 2 commands and nodes from the terminal
- Develop custom ROS 2 packages that include custom nodes, topics and actions using Python
- Interact with and program ROS-enabled robots


## Credits

This repository was forked from [ROSWorkshop](https://github.com/Marwan-Refaat/ROSWorkshop), originally prepared by Marwan Refaat when on a summer internship at Hanze University of Applied Sciences. It was later updated and modified.

## Setup Requirements

#### Software
The software requirements for this course are:

- [Ubuntu 24.04](https://releases.ubuntu.com/24.04/) 
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)
- The [iRobot Create3 Platform interfaces](https://github.com/iRobotEducation/irobot_create_msgs) package is required to work with this robot.

A guide to create a Virtual Machine with Ubuntu and ROS 2 is [available here.](/ros2_vm_guide.md)

#### Hardware (optional)
The demonstration platform used in this course is the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot, so a working Create3 robot is required to run the specific examples.

In cases where such a setup is not feasible, very similar activities can be created and demonstrated using the Gazebo simulation provided in the [Create3 Simulation Packages](https://github.com/iRobotEducation/create3_sim). However, this does require a powerful enough machine to comfortably run Gazebo.

## License
This project is licensed under the terms of the [MIT license](/LICENSE.md).