# Common ROS 2 Commands (CLI Cheat Sheet)

This is a non-exhaustive list of commonly used ROS2 commands. This list was created for ROS 2 Jazzy, but it should work for other ROS 2 distributions.

> Remember to source ROS 2 first (if not included in your .bashrc)

```bash
source /opt/ros/jazzy/setup.bash
```

***

ROS 2 provides a unified CLI (`ros2`) with many subcommands for interacting with the system. [\[docs.ros.org\]](https://docs.ros.org/en/jazzy/Concepts/Basic/About-Command-Line-Tools.html)

## General CLI

```bash
ros2 --help                # Show all ROS 2 commands
ros2 doctor                # Check ROS setup
ros2 pkg list              # List installed packages
ros2 pkg executables <pkg> # List executables in a package
```

***

## Running

```bash
ros2 run <package> <executable>          # Run a single node
ros2 launch <package> <file.launch.py>   # Launch a system (multiple nodes)
```

* `ros2 run`: starts one executable [\[docs.ros.org\]](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Nodes/Understanding-ROS2-Nodes.html)
* `ros2 launch`: starts multiple nodes with configuration from a launch file [\[docs.ros.org\]](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html)

***

## Nodes

```bash
ros2 node list          # List running nodes
ros2 node info <node>   # Detailed node information
```

***

## Topics

```bash
ros2 topic list                         # List topics
ros2 topic list -t                      # List topics + types
ros2 topic echo <topic>                 # Print messages
ros2 topic pub <topic> <type> "<data>"  # Publish message
ros2 topic info <topic>                 # Topic info
ros2 topic hz <topic>                   # Publish rate
```

Topics are the main communication mechanism in ROS 2. [\[docs.ros.org\]](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)

***

## Services

```bash
ros2 service list
ros2 service type <service>
ros2 service call <service> <type> "<args>"
ros2 service info <service>
```

***

## Parameters

```bash
ros2 param list <node>
ros2 param get <node> <param>
ros2 param set <node> <param> <value>
```

***

## Actions

```bash
ros2 action list
ros2 action info <action>
ros2 action send_goal <action> <type> "<goal>"
```

***

## Interfaces

```bash
ros2 interface list
ros2 interface show <type>
```

***

## Bags

```bash
ros2 bag record -a
ros2 bag record <topic1> <topic2>
ros2 bag play <bagfile>
```

***

## Visualization & Debugging Tools

```bash
ros2 run rqt_graph rqt_graph
```

* Provides a **graphical view of nodes and topics**
* Shows how data flows between nodes in real time
* Extremely useful for debugging communication issues

`rqt_graph` visualizes the ROS graph (nodes + topics + connections). [\[docs.ros.org\]](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)


***

### Other Debugging Tools

```bash
ros2 topic find <type>
ros2 service find <type>
ros2 daemon stop
ros2 daemon start
```

***

## Passing ROS Arguments

```bash
ros2 run <pkg> <exec> --ros-args -r __node:=new_name
```

***

# Quick Example

```bash
# Terminal 1
ros2 run demo_nodes_cpp talker

# Terminal 2
ros2 topic echo /chatter

# Terminal 3 (visualization)
ros2 run rqt_graph rqt_graph
```

***

