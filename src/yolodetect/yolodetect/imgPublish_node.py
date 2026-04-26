"""
OBJECTIVE: 
- Take camera frames
- Send to the topics-

APPROACH:
- Make node
- Make node that uses OpenCV to capture frames
- Make topics that accepts image data type
- Send node data to the topic
- test topic data (before connecting subscriper node) just with publisher node
"""
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image   # message type for topic
from cv_bridge import CvBridge      # used for converting cv2_image -> ros2_image
from ultralytics import YOLO

class ImgPublishNode(Node):

    def __init__(self):
        #defining & passing node name within super class's(Node) constructor
        super().__init__('imgpublish_node')

        # Load pretrained YOLO model
        self.model = YOLO("yolov8n.pt")

       
        # connect witht with the camera
        self.camera = cv2.VideoCapture(2)

        # object for  CVBridge() used for cvt cv2->ros2_img
        self.bridge = CvBridge()
        
        # creater publisher node AND topic to publish on
        self.publisher=self.create_publisher(Image,"image", 10)

        # timer that callsback the publish_frame() method for publishing in 0.1sec=10FPS
        self.timer = self.create_timer(0.1, self.publish_frame)


    def publish_frame(self):
        # getting the frame from camera using OpenCV
        ret, frame = self.camera.read()
        
        if not ret or frame is None:
            self.get_logger().warn("Failed to grab frame")
            return
        
        # Run yolov8 model detection
        detection_result = self.model(frame)

        # Show detections
        annotated_detection_result = detection_result[0].plot()

            
        # convert opencv frame to ros2_image
        self.ros_img=self.bridge.cv2_to_imgmsg(annotated_detection_result, encoding='bgr8')

        # publishing the msg
        self.publisher.publish(self.ros_img)

        self.get_logger().info("Frame Published....") # verifying messages


    def destroy_node(self):
        # This is called when node shuts down (Ctrl+C)
        # ALWAYS release camera here — prevents the stuck-camera problem
        if self.camera.isOpened():
            self.camera.release()
            self.get_logger().info('Camera released cleanly')
        super().destroy_node()


def main():

    
    #initialize ros2 rclpy
    rclpy.init()

    # create node object from my class
    my_pubNode=ImgPublishNode()

    try:
        # Start node execution from here by passing my node
        rclpy.spin(my_pubNode)
    except KeyboardInterrupt:
        pass
    finally:
         # After Program shuts, destroy node & clear memory:
        my_pubNode.destroy_node()   # ← guarantees camera.release() is always called
        rclpy.shutdown()


if __name__=="__main__":
    main()