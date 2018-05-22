#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from apriltags_ros.msg import AprilTagDetectionArray

def tagDetected(data):
    datan = "%s" % data
    pub = rospy.Publisher('robAssist/tagDetector', String, queue_size=10)
    try:
        det = datan.split("id: ")[1].split("\n")[0]
        rospy.loginfo("TAG ID %s" % det)
        pub.publish("TAG ID %s" % det)
    except IndexError:
        pub.publish("NO TAG")
        

def aprilReader():
    rospy.init_node("tag_detector", anonymous=False)
    rospy.Subscriber('/tag_detections', AprilTagDetectionArray, tagDetected)
    rospy.spin()


if __name__ == '__main__':
    try:
        aprilReader()
        
    except rospy.ROSInterruptException:
        pass
