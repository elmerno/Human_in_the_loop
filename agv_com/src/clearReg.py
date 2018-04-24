#!/usr/bin/env python

import rospy
import roslib
import socket
import requests
from std_msgs.msg import String
import time
import numpy
import json
from sensor_msgs.msg import JointState

def clearReg():
    registerpos1='http://192.168.12.112:8080/v1.0.0/registers/1'
    registerpos2='http://192.168.12.112:8080/v1.0.0/registers/2'
    resp = requests.post(registerpos1, json={"value" : "0"})
    resp = requests.post(registerpos2, json={"value" : "0"}) 


if __name__ == '__main__':
    try:
        clearReg()
        
    except rospy.ROSInterruptException:
        pass
