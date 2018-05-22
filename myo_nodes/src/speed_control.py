#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Vector3
origindeg = 0
currentdeg = 0
velocity = 0.5
lastGest = "REST"

def updateDef(message):
    global velocity
    pub = rospy.Publisher("robAssist/velocity", String, queue_size=100)
    global currentdeg
    global lastGest
    currentdeg = message.z
    verticaldeg = message.y
    if lastGest == "FIST" and verticaldeg<10 and verticaldeg >-10:
        diff = currentdeg - origindeg
        rospy.loginfo("velocity: %s" % velocity)
        if(diff>20):
            if(velocity<1):
                velocity=velocity+0.005
        elif(diff<-20):
            if(velocity>=0.01):
                velocity=velocity-0.005
        pub.publish("%f" % velocity)

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
    rospy.init_node('speed_control', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom2)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
