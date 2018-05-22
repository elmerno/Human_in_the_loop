#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
deg = 0

def updateDef(message):
    global deg 
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    deg = message.y
    if deg < -50:
        robotpub.publish("STOP")
        rospy.loginfo("Robot is stopping")

def sendCom2(datan):
    pass
    

def robCon():
    rospy.init_node('stop_checker', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom2)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
