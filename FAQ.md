## Frequently Asked Questions

Building and maintaining a reliable conection with ROS 2 robots over wifi using a virtual machine setup can be challenging at times. This section will attempt to provide easy solutions to reccuring problems faced during the course:


**Q: How do I change my `ROS_DOMAIN_ID`?**

**A:** 
The first and easiest variable to rule out is the `ROS_DOMAIN_ID` variable. If your device and the robot you're connecting to use different domain IDs, you will not be able to interact with one another at all.

Your `ROS_DOMAIN_ID` environment variable is usually set in your `.bashrc` file, to edit it, you can use the following command

	gedit ~/.bashrc

This should open your `.bashrc` file using a standard text editor. Scroll down to the bottom of your file and you should see a line similar to this (Add it if it is not there):
	
    export ROS_DOMAIN_ID=1
    
 Change your ID accordingly and save your file
 
  **Note: There should not be multiple lines like the one above, as only the line that is closest to the end of the file will be used. Make sure to scroll to the last line as gedit is sometimes bugged on some machines**
 
 To confirm your changes have taken effect, open a new terminal and entering the following command:
 	
    echo $ROS_DOMAIN_ID
 
 This should now output the correct domain ID.
 
  
**Q: How do I correctly configure my network settings on a virtual machine**

**A:** Most of the time, you will not be able to successfully connect to other ROS 2 devices over the network if your virtual machine does not use a bridged adapter network configuration. [This guide](https://wiki.dave.eu/index.php/VirtualBox_Network_Configuration) is useful for VirtualBox users.  A similar setting is also available in VMWare.

