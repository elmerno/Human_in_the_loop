#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import Vector3

def timer():
    rospy.init_node("ros_timer", anonymous=False)
    pub = rospy.Publisher("timer", Int32, queue_size=10)
    rate = rospy.Rate(1000)
    counter=0
    while not rospy.is_shutdown():
        rate.sleep()
        counter = counter + 1
        pub.publish(counter)

if __name__ == '__main__':
    try:
        timer()
    except rospy.ROSInterruptException:
        pass
