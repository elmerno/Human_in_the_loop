#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import Vector3
lastgest = "N"
origindeg = 0
deg = 0
lastdeg=0
armIn = False
armOut = False
posDegShift = False
negDegShift = False
timeAtFist = 0
time = 0

def updateDef(message):
    global origindeg
    global lastgest
    global deg
    global armIn
    global armOut
    global lastdeg
    global posDegShift
    global negDegShift
    global timeAtFist
    global time
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    if posDegShift or (message.x<-170 and lastdeg>170):
        deg=message.x+360
        negDegShift=False
    elif negDegShift or (message.x>170 and lastdeg<-170):
        deg=message.x-360
        negDegShift=True
        posDegShift=False
    else:
        deg=message.x
    if abs(message.x-lastdeg) < 10:
        negDegShift=False
        posDegShift=False
    lastdeg=deg
    if lastgest == "FIST":
        diff = deg - origindeg
        rospy.loginfo("roted: %d" % diff)
        if diff<-70 and (int(time)-int(timeAtFist))<3000:
            armIn=True
        elif diff>-20 and diff<20 and armIn and int(time)-int(timeAtFist)<6000:
            armOut=True
            rospy.loginfo("Continue signal given")
            robotpub.publish("CONTINUE")

def sendCom(datan):
    global lastgest
    global origindeg
    global deg
    global armIn
    global armOut
    global timeAtFist
    global time
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    data = "%s" % datan
    if "FIST" in data and not lastgest == "FIST":
        lastgest="FIST"
        origindeg=deg
        timeAtFist=time
    elif not "FIST" in data:
        lastgest="NOT FIST"
        armIn=False
        armOut=False
        timeAtFist=0
        
def timer(datan):
    global time
    data = "%s" % datan
    time = data.split(" ")[1]

def robCon():
    rospy.init_node('robot_controller', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.Subscriber("timer", Int32, timer)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
