# ROS 2 Crash Course

Welcome to the ROS 2 Crash Course!

This course is available at: [https://felipenmartins.github.io/ROSWorkshop/](https://felipenmartins.github.io/ROSWorkshop/).

This course covers fundamental concepts of ROS 2 to equip you with the knowledge to run and create your own Python code for robots. It is organized in 2 parts: Part 1 covers ROS 2 and its core concepts, whereas Part 2 is dedicated to the application of such concepts on the Create3 robot.

The course structure is:

## [Part 1 - ROS](/Part_1-ROS/readme.md)

This part covers fundamental ROS 2 concepts. It can be followed even if you don't have access to a physical robot.

- [**Chapter 1 - Fundamental Concepts of ROS**](/Part_1-ROS/Chapter-1/readme.md)
  - ROS overview and history
  - Why use ROS?
  - Main concepts (packages, workspaces, nodes, topics etc.)
  - Activity: Creating your own workspace and running your first nodes

- [**Chapter 2 - Diving into Nodes, Topics and Actions**](/Part_1-ROS/Chapter-2/readme.md)
  - TurtleSim
  - The ROS Graph
  - Nodes, Messages, Topics
  - ROS Actions
  - Writting a node in Python

- [**Chapter 3 - TFs, RViz, Bags and Gazebo**](/Part_1-ROS/Chapter-3/readme.md)
  - Transforms (TFs) and coordinate frames
  - Launch files
  - RViz - ROS Visualization tool
  - ROS Bags
  - Gazebo
  - Adding packages to a workspace

## [Part 2 - Create3](/Part_2-Create3/readme.md)

This part contains a quick introduction to the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot using iRobot's Python Web Playground followed by activities to practice ROS concepts with the robot.

- [**Activity 1 - Introduction to the iRobot Create3**](/Part_2-Create3/Activity_1/readme.md)
- [**Activity 2 - IR sensors and Light Ring**](/Part_2-Create3/Activity_2/readme.md)
- [**Activity 3 - Actions with the physical buttons**](/Part_2-Create3/Activity_3/readme.md)

## Intended Learning Outcomes

By the end of this course, you should be able to:

- Understand fundamental concepts of ROS 2
- Run ROS 2 commands and nodes from the terminal
- Write Python code to develop custom ROS 2 packages that include custom nodes, topics and actions
- Interact with and program ROS-enabled robots

> _Note:_ This is a course about ROS, and not about the fundamentals of robotics. If you are interested in learning more about robotics concepts, check out my [Jupyter Notebooks for learning Mobile Robot Control](https://github.com/felipenmartins/Mobile-Robot-Control) and accompanying [Robotics Simulation Labs](https://felipenmartins.github.io/Robotics-Simulation-Labs/).

## Requirements

### Linux command line

This course assumes that you are familiar with the Linux Terminal commands. You don't need to be an advanced Linux user, but you should know how to:

- access the command line
- investigate and navigate the folder structure (list and access files and folders)
- perform basic file manipulation (create, delete, copy and move files)
- run a command as a super user

If you are new to Linux, I recommend the tutorial [The Linux command line for beginners](https://ubuntu.com/desktop/docs/en/latest/tutorial/the-linux-command-line-for-beginners/), which covers all above topics.

### Software

The software requirements for this course are:

- [Ubuntu 24.04](https://releases.ubuntu.com/24.04/) 
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/index.html)
- The [iRobot Create3 Platform interfaces](https://github.com/iRobotEducation/irobot_create_msgs) package is required to work with this robot.

#### Virtual Machine

A guide to create a Virtual Machine with Ubuntu and ROS 2 is [available here](/Part_1-ROS/ros2_vm_guide.md).

### Hardware (optional)

The demonstration platform used in this course is the [iRobot Create3](https://iroboteducation.github.io/create3_docs/) educational robot, so a working Create3 robot is required to complete the activities in Part 2.

## Acknowledgment

An early version of this course was prepared by Marwan Refaat during a summer internship at Hanze University of Applied Sciences. This repository was forked from his [ROSWorkshop](https://github.com/Marwan-Refaat/ROSWorkshop) and was built on top of his  work.

Thank you, Marwan!

## License

Just like Marwan's work, this project is licensed under the terms of the [MIT license](/LICENSE.md).
