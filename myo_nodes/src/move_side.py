#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import Vector3
lastgest = "N"
origindeg = 0
deg = 0
lastdeg=0
posDegShift = False
negDegShift = False
timeAtGest = 0
time = 0
gestSent = False

def updateDef(message):
    global origindeg
    global lastgest, gestSent
    global deg
    global lastdeg
    global posDegShift
    global negDegShift
    global timeAtGest
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
    if lastgest == "WAVE_IN" or lastgest == "WAVE_OUT":
        diff = deg - origindeg
        rospy.loginfo("rotated: %d" % diff)
        rospy.loginfo("%d" % (int(time)-int(timeAtGest)))
        if diff<-25 and (int(time)-int(timeAtGest))<3000 and lastgest == "WAVE_IN" and not gestSent:
            robotpub.publish("MOVE_LEFT")
            rospy.loginfo("Move left command sent")
            gestSent = True
        elif diff>25 and (int(time)-int(timeAtGest))<3000 and lastgest == "WAVE_OUT" and not gestSent:
            robotpub.publish("MOVE_RIGHT")
            rospy.loginfo("Move right command sent")
            gestSent = True
            

def sendCom(datan):
    global lastgest, gestSent
    global origindeg
    global deg
    global timeAtGest
    global time
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    data = "%s" % datan
    if ("WAVE_IN" in data and "WAVE_OUT" in lastgest) or ("WAVE_OUT" in data and "WAVE_IN" in lastgest):
        lastgest = "N"
        timeAtGest=0
        origindeg=0
        gestSent = False
    elif "WAVE_IN" in data and not lastgest == "WAVE_IN":
        lastgest="WAVE_IN"
        origindeg=deg
        timeAtGest=time
        gestSent = False
    elif "WAVE_OUT" in data and not lastgest == "WAVE_OUT":
        lastgest="WAVE_OUT"
        origindeg=deg
        timeAtGest=time
        gestSent = False
    elif not "WAVE_IN" in data and not "WAVE_OUT" in data:
        lastgest="N"
        timeAtGest=0
        origindeg=0
        gestSent = False
        
def timer(datan):
    global time
    data = "%s" % datan
    time = data.split(" ")[1]

def robCon():
    rospy.init_node('side_checker', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.Subscriber("timer", Int32, timer)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
