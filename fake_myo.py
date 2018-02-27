#!/usr/bin/env python
import rospy
from std_msgs.msg import String
    

def fakeMyo():
    rospy.init_node('robot_controller', anonymous=True)
    gest = rospy.Publisher("myo_raw/myo_gest_str", String, queue_size=100)
    ori = rospy.Publisher("myo_raw/myo_ori_deg", String, queue_size=100)
    gest_rate = rospy.Rate(0.4)
    while not rospy.is_shutdown():
        ori.publish("x: 3.2525252\ny: -65.3424242\nz: 5.51251525")
        gest.publish("FINGERS_SPREAD")
        gest_rate.sleep()

if __name__ == '__main__':
    try:
        fakeMyo()
    except rospy.ROSInterruptException:
        pass
