#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
origindeg = 0
currentdeg = 0
velocity = 1
lastGest = "REST"

def updateDef(message):
    global velocity
    pub = rospy.Publisher("robAsisst/velocity", String, 100)
    global currentdeg
    global lastGest
    currentdeg = message.z
    if lastGest == "FIST":
        diff = currentdeg - origindeg
        rospy.loginfo("Rotaded: %d degrees" % diff)
        if(diff>20):
            if(velocity<2):
                velocity=velocity+0.1
        elif(diff<-20):
            if(velocity>0):
                velocity=velocity-0.1
        pub.publish("%d" % velocity)

def sendCom2(datan):
    data = "%s" % datan
    global origindeg
    global lastGest
    if "FIST" in data and not "FIST" in lastGest:
        origindeg = currentdeg
        lastGest = "FIST"
    elif not "FIST" in data:
        lastGest = "REST"

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
