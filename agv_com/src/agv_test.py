#!/usr/bin/env python

import rospy
import roslib
import socket
import requests
from std_msgs.msg import String
import time
import numpy
import json

def checkreg(reg):
    resp = requests.get('http://192.168.12.112:8080/v1.0.0/registers/%d' % reg)
    if resp.json() == {u'id': reg, u'value': 1.0}:
        return True
    return False
    
def resetregs():
    task = {"value" : "0"} #moveleft
    resp = requests.post('http://192.168.12.112:8080/v1.0.0/registers/1', json=task)
    task = {"value" : "0"} #moveleft
    resp = requests.post('http://192.168.12.112:8080/v1.0.0/registers/2', json=task)
    task = {"value" : "0"} #moveleft
    resp = requests.post('http://192.168.12.112:8080/v1.0.0/registers/3', json=task)
    task = {"value" : "0"} #moveleft
    resp = requests.post('http://192.168.12.112:8080/v1.0.0/registers/4', json=task)
    

def automaton_program():
    rospy.init_node('agv_com', anonymous=False)
    while not rospy.is_shutdown():
        taskleft = {"id": 1, "value" : "1"} #moveleft
        respleft = requests.put('http://192.168.12.112:8080/v1.0.0/registers/1', json=taskleft)
        rospy.loginfo(requests.get('http://192.168.12.112:8080/v1.0.0/registers/1').json())
        while not checkreg(2):
             pass
        resetregs()
        taskright = {"id": 3, "value" : "1"} #moveright
        respright = requests.post('http://192.168.12.112:8080/v1.0.0/registers/3', json=taskright)
        while not checkreg(4):
             pass
        resetregs()
        

if __name__ == '__main__':
    try:
        automaton_program()
        
    except rospy.ROSInterruptException:
        pass
