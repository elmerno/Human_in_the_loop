#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from geometry_msgs.msg import Vector3
lastgest = "N"
origindegx = 0
origindegy = 0
lastdeg=0
posDegShift = False
negDegShift = False
timeAtFist = 0
time = 0
degx = 0
degy = 0
topPos = False
leftPos = False
botPos = False
rightPos = False
lastPos = "N"
counter = 0

def updateDef(message):
    global degx, degy
    global origindegx, origindegy
    global lastgest
    global deg
    global lastdeg
    global posDegShift
    global negDegShift
    global timeAtFist
    global time, counter
    global topPos, leftPos, botPos, rightPos, lastPos
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    if posDegShift or (message.x<-170 and lastdeg>170):
        degx=message.x+360
        negDegShift=False
    elif negDegShift or (message.x>170 and lastdeg<-170):
        degx=message.x-360
        negDegShift=True
        posDegShift=False
    else:
        degx=message.x
    if abs(message.x-lastdeg) < 10:
        negDegShift=False
        posDegShift=False
    lastdegx=degx
    degy=message.y
    if lastgest == "FIST":
        diffx = degx - origindegx
        diffy = degy - origindegy
        rospy.loginfo("rotated: %d x %d y" % (diffx, diffy))
        if diffx < -10 and diffx > -30 and diffy < -10:
            if lastPos=="RIGHT" or lastPos=="TOP" or lastPos=="N":
                topPos = True
                lastPos="TOP"
            else:
                lastPos="N"
                topPos=False
                leftPos=False
                botPos=False
                rightPos=False
                counter=0
        elif diffx < -30 and diffy > -10 and diffy < 10:
            if lastPos=="TOP" or lastPos=="LEFT" or lastPos=="N":
                leftPos = True
                lastPos="LEFT"
            else:
                lastPos="N"
                topPos=False
                leftPos=False
                botPos=False
                counter=0
        elif diffx < -10 and diffx > -30 and diffy > 10:
            if lastPos=="LEFT" or lastPos=="BOT" or lastPos=="N":
                botPos = True
                lastPos="BOT"
            else:
                lastPos="N"
                topPos=False
                leftPos=False
                botPos=False
                counter=0
        elif diffx > -10 and diffy < 10 and diffy > -10:
            if lastPos=="BOT" or lastPos=="N" or lastPos=="RIGHT":
                rightPos = True
                lastPos="RIGHT"
            else:
                lastPos="N"
                topPos=False
                leftPos=False
                botPos=False
                counter=0
        if rightPos and topPos and leftPos and botPos:
            lastPos="N"
            topPos=False
            leftPos=False
            botPos=False
            rightPos=False
            counter=counter+1
        if counter>=2:
            rospy.loginfo("Continue signal given")
            robotpub.publish("CONTINUE")
        rospy.loginfo("%s, %s, %s, %s, %s, %s" % (rightPos, topPos, leftPos, botPos, counter, lastPos))
    else:
        topPos=False
        botPos=False
        rightPos=False
        leftPos=False

def sendCom(datan):
    global degx, degy
    global lastgest
    global origindegx, origindegy
    global timeAtFist
    global time, counter
    global topPos, botPos, rightPos, leftPos
    robotpub = rospy.Publisher("agv_com", String, queue_size=100)
    data = "%s" % datan
    if "FIST" in data and not lastgest == "FIST":
        lastgest="FIST"
        origindegx=degx
        origindegy=degy
        timeAtFist=time
    elif not "FIST" in data:
        lastgest="N"
        timeAtFist=0
        topPos=False
        botPos=False
        rightPos=False
        leftPos=False
        counter=0
        
def timer(datan):
    global time
    data = "%s" % datan
    time = data.split(" ")[1]

def robCon():
    rospy.init_node('continue_checker', anonymous=True)
    rospy.Subscriber("myo_raw/myo_gest_str", String, sendCom)
    rospy.Subscriber("myo_raw/myo_ori_deg", Vector3, updateDef)
    rospy.Subscriber("timer", Int32, timer)
    rospy.spin()

if __name__ == '__main__':
    try:
        robCon()
    except rospy.ROSInterruptException:
        pass
