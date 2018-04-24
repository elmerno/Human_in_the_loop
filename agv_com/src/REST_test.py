#!/usr/bin/env python


#----------------------------------------------------------------------------------------
# authors, program name, version
#----------------------------------------------------------------------------------------
    # Endre Eres
    # Handover with MIR : Program.py
    # V. 0.3



import rospy
import roslib
import socket
import requests
from std_msgs.msg import String
from ur_msgs.msg import IOStates
from ur_msgs.srv import SetIO
import time
import numpy


# --------------------------------------------------------------------------------------------------------------------
# rosservice
# --------------------------------------------------------------------------------------------------------------------

def set_IO_states(fun, pin, state):
    rospy.wait_for_service('/ur_driver/set_io')
    try:
        set_io = rospy.ServiceProxy('/ur_driver/set_io', SetIO)
        resp = set_io(fun, pin, state)
        return resp
    except rospy.ServiceException, e:
        print "Service call Failed: %s"%e


#--------------------------------------------------------------------------------------------------------------------
# the main class
#--------------------------------------------------------------------------------------------------------------------
class automaton_program(Support, Sensors, CModelGripper):

    def __init__(self):
        
        rospy.init_node('automaton_program', anonymous=False)
        #------------------------------------------------------------------------------------------------------------
        # jointCallback helpers
        #------------------------------------------------------------------------------------------------------------
        self.CurrentStateInModel = ''
        self.GripperState = ''
        self.UR10State = ''
        self.MIRState = 'MIRHomeW'
        self.UR10TransportState = ''
        self.UR10ProcessState = ''
        self.BigState = 'bigByMIR'         #initial
        self.SmallState = 'smallByMIR'     #initial
        self.BoltState = 'boltByMIR'       #initial
        self.NutState = 'nutByMIR'         #initial
        self.AsmbldState = 'asmbldNotYet'  #initial
        self.CurrentState = ''
        self.FinishedProcesses = []
        self.Event = ''

        #------------------------------------------------------------------------------------------------------------
        # publishers, subscribers and other ROS parts
        #------------------------------------------------------------------------------------------------------------
        self.URScriptPublisher = rospy.Publisher("/ur_driver/URScript", String, queue_size=200)
        
        rospy.Subscriber("/optoforce_0", WrenchStamped, self.forceCallback)
        rospy.Subscriber("/ur_driver/io_states", IOStates , self.ioCallback)
        rospy.Subscriber("/joint_states", JointState, self.jointCallback)
        rospy.Subscriber("/CModelRobotInput", inputMsg.CModel_robot_input, self.gripperCallback)
        
        self.rate = rospy.Rate(100)
        self.rate.sleep()
        time.sleep(3)
        
        self.Initialize()

        rospy.spin()


    # Unlock protective stop
    def UnlockProtectiveStop(self):
        HOST = "192.168.1.115"
        PORT = 29999 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send ("unlock protective stop" + "\n")
        s.close()    

    # Load the big item fetching program
    def load_demo_script_big(self):
        HOST = "192.168.1.115"
        PORT = 29999 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send ("load /programs/demo_script_big.urp" + "\n")
        s.close()

    # Play the program - only if it is loaded 
    def play_UR10_program(self):
        HOST = "192.168.1.115"
        PORT = 29999 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send ("play" + "\n")
        s.close()

    # Stop the program
    def stop_UR10_program(self):
        HOST = "192.168.1.115"
        PORT = 29999 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send ("stop" + "\n")
        s.close()    


    # --------------------------------------------------------------------------------------------------------------------
    # MiR REST stuff
    # --------------------------------------------------------------------------------------------------------------------

    # Set MiR's PLC Register back to 0
    def reset_PLC_registers(self):
        taska = {"value" : "0"}
        respa = requests.post('http://192.168.1.140:8080/v1.0.0/registers/1', json=taska)
        taskb = {"value" : "0"}
        respb = requests.post('http://192.168.1.140:8080/v1.0.0/registers/2', json=taskb)
        taskc = {"value" : "0"}
        respc = requests.post('http://192.168.1.140:8080/v1.0.0/registers/3', json=taskc)
        taskd = {"value" : "0"}
        respd = requests.post('http://192.168.1.140:8080/v1.0.0/registers/4', json=taskc)

    def call_mir_to_UR(self):
        task = {"value" : "1"}
        resp = requests.post('http://192.168.1.140:8080/v1.0.0/registers/1', json=task)

    def send_mir_back(self):
        task = {"value" : "1"}
        resp = requests.post('http://192.168.1.140:8080/v1.0.0/registers/3', json=task)

    # Set desired MiR state
    def mir_pause_state(self):
        task = {"state" : 4}
        resp = requests.put('http://192.168.1.140:8080/v1.0.0/state', json=task)

    # Set desired MiR state
    def mir_executing_state(self):
        task = {"state" : 5}
        resp = requests.put('http://192.168.1.140:8080/v1.0.0/state', json=task)

    # Put Mission to queue
    def mission_to_queue(self):
        task ={"mission" : "63ce173b-0055-11e8-95bf-f44d306bb564"} 
        resp = requests.post('http://192.168.1.140:8080/v1.0.0/mission_queue', json=task)

    # Delete the Mission Queue
    def delete_mir_mission_queue(self):
        resp = requests.delete('http://192.168.1.140:8080/v1.0.0/mission_queue')

    # Starting Mission
    def start_mission(self):
        self.delete_mir_mission_queue()
        time.sleep(1)
        self.reset_PLC_registers()
        time.sleep(1)
        self.mission_to_queue()
        time.sleep(1)
        self.mir_executing_state()

    # Set desired MiR state
    def mir_pause_state(self):
        task = {"state" : 4}
        resp = requests.put('http://192.168.1.140:8080/v1.0.0/state', json=task)

    # Set desired MiR state
    def mir_executing_state(self):
        task = {"state" : 5}
        resp = requests.put('http://192.168.1.140:8080/v1.0.0/state', json=task)

    #----------------------------------------------------------------------------------------------------------------
    # initialize the robot and move it to the home position
    #----------------------------------------------------------------------------------------------------------------
    def Initialize(self):
        self.resetGripper()
        rospy.sleep(2)
        self.activateGripper()
        command = self.urSrciptToString(move = "movej", jointPose = self.URHomeW, a = 1.5, v = 7, t = 3, r = 0)
        self.URScriptPublisher.publish(command)
        self.start_mission()
        self.reset_PLC_registers()
        rospy.sleep(3)
    

    def MIRHomeToUR(self):
        self.call_mir_to_UR()
        while self.var_1 == True:
            self.MIRState = 'MIRHomeToURM'
            resp = requests.get('http://192.168.1.140:8080/v1.0.0/registers/2')
            if resp.json() == {u'id': 2, u'value': 1.0}:
                self.MIRState = 'MIRByURW'
                self.FSMCompleteEventsPublisher.publish('completeTO:MIRHomeToUR')
                self.var_1 = False
                break
            else:
                pass

    def URHomeToAboveMIRBig(self):
        command = self.urSrciptToString(move = "movej", jointPose = self.URAboveMIRW, a = 1.5, v = 7, t = 1.5, r = 0)
        self.URScriptPublisher.publish(command)
        self.UR10TransportState = 'URHomeToAboveMIRM'
        rospy.sleep(2)
        #rospy.loginfo('completeTO:URHomeToAboveItems')
        self.FSMCompleteEventsPublisher.publish('completeTO:URHomeToAboveMIR')

    def MIRURToHome(self):
        self.send_mir_back()
        while self.var_13 == True:
            self.MIRState = 'MIRURToHomeM'
            resp = requests.get('http://192.168.1.140:8080/v1.0.0/registers/4')
            if resp.json() == {u'id': 4, u'value': 1.0}:
                self.MIRState = 'MIRHomeW'
                self.FSMCompleteEventsPublisher.publish('completeTO:MIRURToHome')
                self.var_13 = False
                break
            else:
                pass

    #------------------------------------------------------------------------------------------------------------
    # ioCallback gives us the UR's pin states
    #------------------------------------------------------------------------------------------------------------
    def ioCallback(self,pin_data):
        self.pin_dataG = pin_data
        if pin_data.digital_out_states[7].state == True:
            self.closeGripper()
            set_IO_states(1, 7, 0)
        if pin_data.digital_out_states[6].state == True:
            self.URScriptProgramDone = True
        else:
            self.URScriptProgramDone = False


    #------------------------------------------------------------------------------------------------------------
    # gripperCallback indicates the items location (not in this situation)
    #------------------------------------------------------------------------------------------------------------
    def gripperCallback(self, obj):
        self.gripper_data = obj
        if obj.gPO < 10:
            self.GripperState = 'open'
        elif obj.gPO > 110 and obj.gPO < 120:
            self.GripperState = 'big'
        elif obj.gPO > 125 and obj.gPO < 135:
            self.GripperState = 'small'
        elif obj.gPO > 210 and obj.gPO < 220:
            self.GripperState = 'bolt'
        elif obj.gPO > 190 and obj.gPO < 205:
            self.GripperState = 'nut'
        else:
            self.GripperState = 'irrelevant'


if __name__ == '__main__':
    try:
        automaton_program()
        
    except rospy.ROSInterruptException:
        pass

    


