#!/usr/bin/env python

import roslib
import rospy
import socket
import requests
from std_msgs.msg import String, Header, UInt8
import time
import numpy
import json
from sensor_msgs.msg import JointState
stop = False
pos=[1.0,1.0,1.0,1.0,1.0,1.0]
tag="NO TAG"
velocity=0.5
HOST = "192.168.1.120"
PORT = 30002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def checkCom(data):
    global stop, tag
    pub = rospy.Publisher('ur_driver/URScript', String, queue_size=10)
    vibratepub = rospy.Publisher("/myo_raw/vibrate", UInt8, queue_size=100)
    moveleft = {"mission" : "3910b18b-1d5c-11e8-b829-f44d306f3ce3"}
    moveright = {"mission" : "20c999e2-1622-11e8-aeb8-f44d306f3ce3"}
    mission_queue = 'http://192.168.1.112:8080/v1.0.0/mission_queue'
    register5='http://192.168.1.112:8080/v1.0.0/registers/5'
    register6='http://192.168.1.112:8080/v1.0.0/registers/6'
    datan = "%s" % data
    r = rospy.Rate(1)
    if "STOP" in datan:# and "TAG ID" in tag:
        rospy.loginfo("Robot is stopping")
        resp = requests.delete(mission_queue)
        pub.publish("stopj(2)")
        stop = True
        rospy.loginfo("Robot is stopping")
    
    elif "CONTINUE" in datan:# and "TAG ID" in tag:
        # rospy.loginfo("Robot is continuing")
        # resp = requests.delete(mission_queue)
        stop = False
        vibratepub.publish(1)
    
    elif "MOVE_LEFT" in datan:# and "TAG ID" in tag:
        rospy.loginfo("Robot is moving left")
        resp = requests.delete(mission_queue)
        pub.publish("stopj(2)")
        stop = True
        r.sleep()
        resp = requests.post(mission_queue, json=moveleft)
    
    elif "MOVE_RIGHT" in datan:# and "TAG ID" in tag:
        rospy.loginfo("Robot is moving right")
        resp = requests.delete(mission_queue)
        pub.publish("stopj(2)")
        stop = True
        r.sleep()
        resp = requests.post(mission_queue, json=moveright)
     
def position(current_pos):
    global pos
    pos=current_pos.position
        
def correctPos(goal_pos):
    global pos
    for x in range(0,6):
        if(abs(pos[x]-goal_pos[x])<0.001):
            if(x==5):
                return True
                rospy.loginfo("True")
        else:
            return False
        
def speed(data):
    global tag
    if True: #"TAG ID" in tag:
        global velocity, s
        data = "%s" % data
        eg2=data.split(" ")
        velocity=eg2[1]
        s.send("set speed % s" % velocity + "\n")
   
def tagDetector(datan):
    global tag
    data = "%s" % datan
    tagdata = data.split("data: ")
    tag = tagdata[1]


def agvloop(): 
    global stop, tag
    rospy.init_node("AGV_loop", anonymous=False)
    rospy.Subscriber("agv_com", String, checkCom)
    rospy.Subscriber("robAssist/velocity", String, speed)
    rospy.Subscriber("joint_states", JointState, position)
    rospy.Subscriber("robAssist/tagDetector", String, tagDetector)
    pub = rospy.Publisher('ur_driver/URScript', String, queue_size=10)
    mission_queue = 'http://192.168.1.112:8080/v1.0.0/mission_queue'
    registerpos1='http://192.168.1.112:8080/v1.0.0/registers/1'
    registerpos2='http://192.168.1.112:8080/v1.0.0/registers/2'
    movepos1 = {"mission" : "ba24db22-22de-11e8-ad87-f44d306f3ce3"}
    movepos2 = {"mission" : "f5486aa1-22de-11e8-ad87-f44d306f3ce3"}
    # 1:a - vicka pa anden 1-2
    move_1="movej([7.792982353834741E-15, -1.5707963267948983, 0.0, -1.5707963267948966, 2.4148088630737306E-18, 2.0913969723046172E-18], a=1.3962634015954636, v=0.3)"
    pos_1=[7.792982353834741E-15, -1.5707963267948983, 0.0, -1.5707963267948966, 2.4148088630737306E-18, 2.0913969723046172E-18]
    move_2="movej([7.792982353834741E-15, -1.5707963267948983, 0.0, -1.5707963267948966, -0.27919999999999945, 0.05493542724666245], a=1.3962634015954636, v=0.3)"
    pos_2=[7.792982353834741E-15, -1.5707963267948983, 0.0, -1.5707963267948966, -0.27919999999999945, 0.05493542724666245]
    # 2:a - sida till sida 3-5
    move_3="movej([-1.5893514963554116, -2.4591132234341977, -1.4866896088162154, -0.7920197419969579, 1.5953902293395572, -0.01965157422308561], a=1.3962634015954636, v=0.3)"
    pos_3=[-1.5893514963554116, -2.4591132234341977, -1.4866896088162154, -0.7920197419969579, 1.5953902293395572, -0.01965157422308561]
    move_4="movej([-1.5830646929376062, -1.5707963267948966, 0.0, -1.5707963267948966, 6.4050765537497964E-18, 0.0], a=1.3962634015954636, v=0.3)"
    pos_4=[-1.5830646929376062, -1.5707963267948966, 0.0, -1.5707963267948966, 6.4050765537497964E-18, 0.0]
    move_5="movej([-1.5830646928920755, -0.9038935365266632, 1.5951369823723027, -1.819683720112998, 4.693264910464599, -0.4384449910357624], a=1.3962634015954636, v=0.3)"
    pos_5=[-1.5830646928920755, -0.9038935365266632, 1.5951369823723027, -1.819683720112998, 4.693264910464599, -0.4384449910357624]
    # 3:e - fram-bak, plocka, rotera 6-9
    # 1:a ut
    move_6="movej([-1.6007002035724085, -2.2223208514361463, -1.7081914229189907, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131], a=1.3962634015954636, v=0.3)" 
    pos_6=[-1.6007002035724085, -2.2223208514361463, -1.7081914229189907, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131]
    # 1:a in
    move_7="movej([-1.6007002035724085, -1.3028030526930543, -2.6753914229189935, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131], a=1.3962634015954636, v=0.3)"
    pos_7=[-1.6007002035724085, -1.3028030526930543, -2.6753914229189935, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131]
    # 2:a in
    move_8="movej([1.7093316203474103, -1.3028030526930543, -2.6753914229189935, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131], a=1.3962634015954636, v=0.3)"
    pos_8=[1.7093316203474103, -1.3028030526930543, -2.6753914229189935, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131]
    # 2:a ut
    move_9="movej([1.7093316203474103, -2.337276688325647, -1.5609914229189918, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131], a=1.3962634015954636, v=0.3)"
    pos_9=[1.7093316203474103, -2.337276688325647, -1.5609914229189918, -0.8087108120924764, 1.5951000452041626, -0.03099996248354131]
    HOST = "192.168.1.120"
    PORT = 30002
    resp = requests.post(registerpos1, json={"value" : "0"})
    resp = requests.post(registerpos2, json={"value" : "0"}) 
    rate = rospy.Rate(2)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send ("set speed 0.5" + "\n")
      
    while not rospy.is_shutdown():
        
        #UR positioner 1-2 1:a, 3-5 2:a, 6-9 3:e
        #AGV to position1 & UR to position 7
        rospy.loginfo("AGV to position 1 & UR going to first side")
        if not stop:
            resp = requests.post(mission_queue, json=movepos1)
            pub.publish(move_7)
        while (not requests.get(registerpos1).json() == {u'id': 1, u'value': 1.0} or not correctPos(pos_7)) and not rospy.is_shutdown():
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("AGV continuing to position 1 & UR continuing to first side")
                resp = requests.post(mission_queue, json=movepos1)
                pub.publish(move_7)
        resp = requests.post(registerpos1, json={"value" : "0"})
        
        #UR to position 6
        rospy.loginfo("UR going out")
        if not stop:
            pub.publish(move_6)
        while not correctPos(pos_6) and not rospy.is_shutdown():
            
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("UR continuing going out")
                pub.publish(move_6)
        
        #UR to position 7
        rospy.loginfo("UR going in")
        if not stop:
            pub.publish(move_7)
        while not correctPos(pos_7) and not rospy.is_shutdown():
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("UR continuing going in")
                pub.publish(move_7)
        
        #AGV to position2 % UR to position 8
        rospy.loginfo("AGV to position 2 & UR going to second side")
        if not stop:
            resp = requests.post(mission_queue, json=movepos2)
            pub.publish(move_8)
        while (not requests.get(registerpos2).json() == {u'id': 2, u'value': 1.0} or not correctPos(pos_8)) and not rospy.is_shutdown():
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("AGV continuing to position 2 & UR continuing to second side")
                resp = requests.post(mission_queue, json=movepos2)
                pub.publish(move_8)
        resp = requests.post(registerpos2, json={"value" : "0"})
        
        
        #UR to position 9
        rospy.loginfo("UR going out")
        if not stop:
            pub.publish(move_9)
        while not correctPos(pos_9) and not rospy.is_shutdown():
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("UR continuing going out")
                pub.publish(move_9)
        
        #UR to position 8
        rospy.loginfo("UR going in")
        if not stop:
            pub.publish(move_8)
        while not correctPos(pos_8) and not rospy.is_shutdown():
            if stop:
                while stop and not rospy.is_shutdown():
                    pass
                rospy.loginfo("UR continuing going in")
                pub.publish(move_8)
        
        
    resp = requests.delete('http://192.168.1.112:8080/v1.0.0/mission_queue')
    pub.publish("stopj(2)")
    s.close()

if __name__ == '__main__':
    try:
        agvloop()
        
    except rospy.ROSInterruptException:
        pass
