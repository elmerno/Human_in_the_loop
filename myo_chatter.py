#!/usr/bin/env python
import rospy
from std_msgs.msg import String
deg = 0

def updateDef(datan):
    data = "%s" % datan #x: ###\n y: ###\n z: ### 
    eg = data.split("\n")
    rospy.loginfo(eg[1])

def sendCom2(datan):
    pub = rospy.Publisher("rob_commands", String, queue_size=100)

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
    rospy.Subscriber("myo_raw/myo_ori_deg", String, updateDef)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
