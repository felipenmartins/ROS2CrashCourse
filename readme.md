# ROS 2 Crash Course

Welcome to the ROS 2 Crash Course!

This course covers fundamental ROS 2 concepts to equip you with the knowledge to run and create your own Python code to control robots. It is organized in 2 parts: one that covers ROS 2 and its core concepts, and another dedicated to applying such concepts on the Create3 robot.

The course structure is:

## [Part 1 - ROS](/Part_1-ROS/readme.md)
This part covers fundamental ROS 2 concepts. It can be followed even if you don't have access to a physical robot.

- [**Chapter 1: What is ROS?**](/Chapter-1/readme.md)
  - The history of ROS
  - Why use ROS?
  - Overview of ROS
  - Summary of CLI commands
- [**Chapter 2: FUndamental Concepts of ROS**](/Chapter-2/readme.md)
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

## [Part 2 - Create3](/Part_2-Create3/readme.md)
This part provides activities for the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot, so you can apply the concepts discussed in part 1. 

- [**Overview of the Create3**](/Chapter-4/readme.md)
- Activity 1 - IR sensors and LED pannel
- Activity 2 - Actions with the physical buttons   

---

### Intended Learning Outcomes:
By the end of this course, you should be able to: 
- Understand fundamental concepts of ROS 2
- Run ROS 2 commands and nodes from the terminal
- Develop custom ROS 2 packages that include custom nodes, topics and actions using Python
- Interact with and program ROS-enabled robots


## Credits
This repository was forked from [ROSWorkshop](https://github.com/Marwan-Refaat/ROSWorkshop), originally prepared by Marwan Refaat when on a summer internship at Hanze University of Applied Sciences. It was later updated and modified.

## Setup Requirements
### Software
The software requirements for this course are:

- [Ubuntu 24.04](https://releases.ubuntu.com/24.04/) 
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)
- The [iRobot Create3 Platform interfaces](https://github.com/iRobotEducation/irobot_create_msgs) package is required to work with this robot.

A guide to create a Virtual Machine with Ubuntu and ROS 2 is [available here.](/Part_1-ROS/ros2_vm_guide.md)

### Hardware (optional)
The demonstration platform used in this course is the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot, so a working Create3 robot is required to complete the activities in Part 2.

## License
This project is licensed under the terms of the [MIT license](/LICENSE.md).