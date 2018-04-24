#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt8
from sensor_msgs.msg import JointState
v="0.2"
Stop_var="ej"
pos=[1.0,1.0,1.0,1.0,1.0,1.0]

def speed(data):
   global v  
   data = "%s" % data
   eg2=data.split(" ")
   data=eg2[1]
   v=data
   rospy.loginfo(v)


def Stop(Stop_data):
    global Stop_var
    Stop_var = "%s" % Stop_data
    rospy.loginfo(Stop_var)
    pub = rospy.Publisher('ur_driver/URScript', String, queue_size=10)
    

    
    
    if "stop" in Stop_var:
 	    pub.publish("stopj(2)")
        pub2=rospy.Publisher("myo_raw/vibrate", UInt8, queue_size=10)
	    pub2.publish(3)
def position(current_pos):
    global pos
    pos=current_pos.position

def correctPos(goal_pos):
    global pos
    for x in range(0,6):
        if(abs(pos[x]-goal_pos[x])<0.001):
            if(x==5):
                return True
                rosyp.loginfo("True")
        else:
            return False
	    rosyp.loginfo("Felse")
def getdata():
    global v
    global Stop_var
    global pos
    rospy.init_node("talk_to_simulator_speed_variable", anonymous=True)
    rospy.Subscriber("robAsisst/velocity", String, position)
    rospy.Subscriber("joint_states", JointState, position)
    rospy.Subscriber("ur_stop", String, Stop)
    pub = rospy.Publisher('ur_driver/URScript', String, queue_size=10)
    rate = rospy.Rate(1) # 10hz
    rate2 = rospy.Rate(10)

    move_1="movej([1.1152377366574322E-15, -1.5707963267948966, 1.6715757583150786E-20, -1.5707963267948948, 9.72002403636376E-16, 0.0], a=1.3962634015954636, v=%s)" % v
    pos_1=[0.0, -1.5707963267948966, 0.0, -1.5707963267948948, 0.0, 0.0]
    move_2="movej([-1.0805520566758986E-4, -1.5707963267948966, 1.5752000000000015, -1.5707963267948948, 9.72002403636376E-16, 0.0], a=1.3962634015954636, v=%s)" % v
    pos_2=[0.0, -1.5707963267948966, 1.5752000000000015, -1.5707963267948948,0.0,0.0]


    while not rospy.is_shutdown():
	#rospy.loginfo("awaiting") 
	#rate.sleep()
		
    	if not rospy.is_shutdown(): # and not "stop" in Stop_var:
                
		rospy.loginfo("moving to point 1")

	        pub.publish(move_1)


		while not correctPos(pos_1) and not rospy.is_shutdown():
		    rate2.sleep()
		    rospy.loginfo("Loop_1")
		
                rate.sleep()
		if "stop" in Stop_var:
			while "stop" in Stop_var and not rospy.is_shutdown():
			    rate2.sleep()	
	    	            rospy.loginfo("loop_2")
			pub.publish(move_1)
			rospy.loginfo("continue with: moving to point 1")
			while not correctPos(pos_1) and not rospy.is_shutdown():
			    rate2.sleep() 
		            rospy.loginfo("loop_3")
                        rate.sleep()
		

		rospy.loginfo("moving to point 2")
        	pub.publish(move_2)
		while not correctPos(pos_2) and not rospy.is_shutdown():
			rate2.sleep()
		        rospy.loginfo("loop_4")
                rate.sleep()
		if "stop" in Stop_var:
			while "stop" in Stop_var and not rospy.is_shutdown():
				rate2.sleep()
  				rospy.loginfo("loop_5")		
			pub.publish(move_2)
			rospy.loginfo("continue with: moving to point 2")
			while not correctPos(pos_2) and not rospy.is_shutdown():
			    rate2.sleep()
		            rospy.loginfo("loop_6")
                        rate.sleep()
    

if __name__ == '__main__':
    try:
        getdata()
    except rospy.ROSInterruptException:
        pass
