#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
    

def fakeMyo():
    rospy.init_node('robot_controller', anonymous=True)
    gest = rospy.Publisher("myo_raw/myo_gest_str", String, queue_size=100)
    ori = rospy.Publisher("myo_raw/myo_ori_deg", Vector3, queue_size=100)
    gest_rate = rospy.Rate(0.4)
    while not rospy.is_shutdown():
        ori.publish(Vector3(3.2525252, -65.3424242, 5.51251525))
        gest.publish("FINGERS_SPREAD")
        gest_rate.sleep()

if __name__ == '__main__':
    try:
        fakeMyo()
    except rospy.ROSInterruptException:
        pass
