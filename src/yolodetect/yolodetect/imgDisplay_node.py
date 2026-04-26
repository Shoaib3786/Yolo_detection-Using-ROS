"""
OBJECTIVE:
- To get the image from topic
- Display the image

APPROACH:
- Make Subcriber node
- Connect with /image topic
- get its data
- convert back ros2_img to cv2 image
- Display image on imshow
- (see if any alternative image show we have from ROS2)
"""

import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge      # used for converting cv2_image -> ros2_image


class ImgDisplayNode(Node):

    def __init__(self):
        super().__init__('imgdisplay_node') # making subcriber node

        self.bridge=CvBridge()  # converter for ros2_img -> cv2

        # subcriber that callsback displayImage() method
        self.subscriber=self.create_subscription(Image,"image", self.displayImage, 10)


    def displayImage(self, got_img):
        self.frame = self.bridge.imgmsg_to_cv2(got_img, desired_encoding='bgr8')
        self.get_logger().info("Got image data....")
        
        cv2.imshow("Display_Node", self.frame)
        cv2.waitKey(1)


    # def destroy_node(self):
    #     # This is called when node shuts down (Ctrl+C)
    #     # ALWAYS release camera here — prevents the stuck-camera problem
    #     if self.camera.isOpened():
    #         self.camera.release()
    #         self.get_logger().info('Camera released cleanly')
    #     super().destroy_node()


def main():

    # initialize rcply
    rclpy.init()

    # make node object of your class
    my_disNode=ImgDisplayNode()

    try:
        # Start node execution from here by passing my node
        rclpy.spin(my_disNode)
    except KeyboardInterrupt:
        pass
    finally:
         # After Program shuts, destroy node & clear memory:
        my_disNode.destroy_node()   # ← guarantees camera.release() is always called
        rclpy.shutdown()



if __name__=='__main__':
    main()
        

        