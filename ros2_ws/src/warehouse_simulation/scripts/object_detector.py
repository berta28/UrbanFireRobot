#!/usr/bin/env python

import rospy

from ultralytics import YOLO
from ultralytics import settings
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class object_detector:
    def __init__(self):
        # self.model = YOLO("yolo11n.pt")
        self.model = YOLO("/root/ros2_ws/src/warehouse_simulation/models/object_detection/yolov8n.pt")

        self.bridge = CvBridge()    

        sub_topic_name="/realsense/image_raw"
        self.camera_subscriber = rospy.Subscriber(sub_topic_name, Image, self.camera_cb)

        self.img_pub = rospy.Publisher("/inference_result", Image, queue_size=1)
        

    def camera_cb(self, data):
        img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        # cv2.imshow("output", img)
        # cv2.waitKey(1)

        results = self.model(img)

        # for r in results:
        #     boxes = r.boxes
        #     for box in boxes:
        #         b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
        #         c = box.cls

        annotated_frame = results[0].plot()

        cv2.imshow("output", annotated_frame)
        cv2.waitKey(1)

        img_msg = self.bridge.cv2_to_imgmsg(annotated_frame)
        self.img_pub.publish(img_msg)

if __name__ == '__main__':
    node_name = "object_detector"
    rospy.init_node(node_name)
    object_detector()
    rospy.spin()