#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
deg = 0

def updateDef(message):
    global deg 
    deg = message.y

def sendCom2(datan):
    pub = rospy.Publisher("rob_commands", String, queue_size=100)
    data = "%s" % datan
    if deg < -25 and "FINGERS_SPREAD" in data:
        pub.publish("STOP")
        rospy.loginfo("Robot is stopping")
            

def sendCom(datan):
    pub = rospy.Publisher("rob_commands", String, queue_size=100)
    data = "%s" % datan
    if "WAVE_OUT" in data:
        rospy.loginfo("Robot is stopping")
        pub.publish("STOP")
    elif "WAVE_IN" in data:
        rospy.loginfo("Robot is moving out of the way")
        pub.publish("MOVE")
    elif "FIST" in data:
        rospy.loginfo("Robot is going to station 1")
        pub.publish("ST1")
    elif "FINGERS_SPREAD" in data:
        rospy.loginfo("Robot is going to station 2")
        pub.publish("ST2")
    elif "THUMB_TO_PINKY" in data:
        rospy.loginfo("Robot is going to station 3")
        pub.publish("ST3")
    

def robCon():
    rospy.init_node('robot_controller', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom2)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
