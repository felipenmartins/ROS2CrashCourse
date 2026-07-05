# Chapter 1 - What is ROS?
This chapter introduces ROS and its core concepts, and gives an insight into why it is important to learn ROS.

### Objectives
By the end of this chappter you should be familiar with:
- The abstracted overview of ROS
- ROS' design philosophies
- The uses of ROS in the industry
- The core concepts of ROS

## 1.1 - Overview of ROS
ROS is short for **Robot Operating System**. Just like a computer operating system, ROS manages hardware and software resources, and provides common services for other programs to interact with each other and with the robot hardware (sensors and actuators). 

However, despite its name, ROS is **_not_** an operating system, but a middleware with a set of communication tools and a collection of plug-and-play libraries that shorten the time-to-market of robotics projects and allows developers to work on the algorithms they are interested in.

ROS is an open-source robotics framework that allows developers and researchers to build and reuse code between robotics applications. Besides its pre-built tools to handle inter-process communication, ROS has many tool that are relevant to robots, like device drivers, simulation and visualization, data logging etc.. Finally, there is a vast community that provides packages for common robotics applications.
 
## 1.2 - The ROS Development Approach
ROS’s design philosophy is unique and is at the heart of why it has become so commonplace in the robotics community.

ROS is :

1. **Multiplatform**
 	- Works on Linux, Windows, MATLAB, etc..
2. **Modular**
	- ROS projects are designed to be completely modular, which allows for reusability and both accelerates and facilitates team work.
3. **Multi-lingual**
	- ROS projects can be written in many languages. Although the main supported languages are Python and C++, there are client libraries for MATLAB, Go, Ruby, NodeJS and many more.
4. **Multidomain**
	 - Can be used for all kinds of robotics applications, from underwater vehicles to moonlanders!
5. **Open-Source**
	- ROS is completely open source, all its tools and almost all of the community-provided libraries are free to use.


### A brief history of ROS
ROS was first developed by two Stanford researchers to accelerate the initial phase of development of most robotics projects, which mostly consisted of what  they described as "reinventing the wheel". ROS was later picked up by robotics incubator [Willow Garage](https://en.wikipedia.org/wiki/Willow_Garage), which continued its development until it was dissolved and the project was picked up again by [Open Robotics](https://www.openrobotics.org/), which is the current entity behind ROS.

As ROS began initially as a platform for researchers, it had become apparent by 2015 that its current capabilities were not adequate for widespread commercial use. The second generation of ROS, ROS 2,was created as a direct result of such realization. ROS 2 was built from the ground-up to solve the identified issues and to be able to handle industrial and commercial applications.

### Why ROS?
The most important question to ask when adopting a new technology is why? Why should I spend the time and effort to learn and  become familiar with this new technology, after all, new technologies come and go very quickly in the software world.

ROS 2’s development was and continues to be guided by a ‘Technical Steering Committee’ composed by several representatives of the robotics community. The wide spread usage of ROS in the robotics field makes it one of the most important tools to master for developers or engineers wanting to enter the field of robotics.

ROS currently powers robots in various domains, from [Astrobee](https://www.nasa.gov/astrobee), NASA’s free-flying robots that have been active in the ISS for years, to [Open-RMF](https://www.open-rmf.org/), a modular software system that enables sharing and interoperability between multiple fleets of robots and physical infrastructure, like doors, elevators and building management systems. 

[ROSIndustrial](https://rosindustrial.org/) is an extension of the ROS platform specifically made to facilitate the transfer of robotics research into the industrial field. It currently boasts over 80 industrial leaders from all around the world such as ABB, Siemens, Boeing, BMW, Panasonic, Universal Robots and many more. 

![ROS Industrial Consortium](https://images.squarespace-cdn.com/content/v1/51df34b1e4b08840dcfd2841/e4f98f71-31eb-436f-aa1c-4d4f969343ac/Logo-montage_2026-April27-tp-s.jpg?format=1500w)
##### Figure 1. Institutions that are part of the ROS Industrial Consortium. _Source: [ROS Industrial](https://rosindustrial.org/current-members)_

## 1.4 - An Overview of ROS
Let's go over a few important ROS concepts. We will dive into those concepts in the next chapter. 

### Nodes
Since ROS is designed to be very modular, a robot control system is broken down into single purpose, independently executable programs, called _nodes_. Nodes can be written in any ROS-compatible language, like C++ or Python, and are made to complete a single, independent task. For example, one node controls a laser range-finder, another node controls the wheel motors, and yet another node performs localization etc..

### Messages
Nodes communicate using messages. A ROS message is just a data structure that contains one or more fields. These fields usually have a type belonging to one of the primitive data types (Integer, Floating Point, Boolean, String). Messages can also include arrays and may be nested to add hierarchy or separation to the data.

### Topics
ROS messages are sent through topics, which follow a simple publish/subscribe protocol. Nodes can publish messages to a topic to share that data across the application, and other nodes can subscribe to that topic to access that data. A single topic can have multiple subscribers and multiple publishers. 

Figure 2 illustrates the concepts of nodes, messages and topics. In the figure, one or two nodes (publishers) publish messages to a topic that has two subscriber nodes. In this configuration, both subscriber nodes receive all messages from both publishers. 

![Multiple node-topic communication](https://docs.ros.org/en/jazzy/_images/Topic-MultiplePublisherandMultipleSubscriber.gif)
##### Figure 2. Nodes exchanging messages via topics. _Source: [ROS 2 Documentation: Jazzy](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)_

For example, a node `/lidar_sensor` might process data from the lidar sensor and publish distance data to a topic called `/distance_data`. The `/localization` node subscribed to the `/distance_data` topic can use that data to help compute the robot’s current location.

### Bags
ROS Bags are a format for saving and playing back ROS message data. Bags are useful in applications that require data persistence and are usually used to store sensor data that requires cumulative processing that is sometimes needed to develop or refine algorithms. For example, you can save all sensor data and commands to a ROS Bag and later replay it using a RViz (a ROS Vizualization tool) to investigate performance and diagnose problems.

### The ROS Computation Graph
The ROS Computation Graph is the network of peer-to-peer processes that compute data and together make up a complete application. The graph consists of the nodes, topics, messages, bags, and services that together constitute a complete ROS project.

### The ROS Filesystem 
A ROS workspace is a directory with a particular structure that houses any ROS project. The minimum requirement for a ROS workspace is a `/src` directory that contains the source code for all the packages in the project. The build tool used in ROS 2 is `colcon`, which has many features that help building and managing ROS workspaces. 

### ROS CLI Commands
Most of our interaction with ROS will be through the terminal or command line, so it is useful to get familiar with the common Linux terminal commands and with common ROS terminal commands. 

If you are new to Linux, I recommend the tutorial [The Linux command line for beginners](https://ubuntu.com/desktop/docs/en/latest/tutorial/the-linux-command-line-for-beginners/). Don’t worry about memorizing all commands now! they will be referenced again as they are used throughout the activities. 

In the next chapters we will study several ROS 2 commands that run in the terminal. A summary of [useful ROS 2 commands is available here](/Part_1-ROS/Chapter-1/ros2_commands.md).

## Conclusion
After completing this chapter, you should have a general understanding of ROS and its importance for the robotics community. In Chapter 2 we will dive into some core topics to better understand how to work with ROS and how to write Python code for ROS.

## Navigation menu
- Continue to [Chapter 2 - Fundamental Concepts of ROS](/Part_1-ROS/Chapter-2/readme.md)
- Go back to [Part 1 - ROS](/Part_1-ROS/readme.md)
- Go to the [Main page](/readme.md)