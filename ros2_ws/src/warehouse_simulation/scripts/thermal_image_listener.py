import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os
import re
from subprocess import call
import time
import math

class ImageListener:
    def __init__(self):
        self.bridge = CvBridge()
        self.angle = 0
        self.distance = 7.0
        self.max_distance = 12.0
        self.base_path = "/home/vboxuser/UrbanFireRobot/images"
        self.test_folder = self.create_new_test_folder()
        self.distance_folder = self.create_new_distance_folder()
        self.image_count = {"thermal_camera": 0, "rgb_camera": 0}
        self.subscribers = {
            "thermal_camera": rospy.Subscriber("/thermal_camera/image", Image, self.callback, "thermal_camera"),
            "rgb_camera": rospy.Subscriber("/camera/image", Image, self.callback, "rgb_camera")
        }

        self.move_robot()

    def create_new_test_folder(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        existing_folders = [f for f in os.listdir(self.base_path) if re.match(r'test_\d+', f)]
        existing_folders.sort()
        if existing_folders:
            last_folder = existing_folders[-1]
            last_index = int(last_folder.split('_')[1])
            new_folder = f"test_{last_index + 1}"
        else:
            new_folder = "test_1"
        new_folder_path = os.path.join(self.base_path, new_folder)
        os.makedirs(new_folder_path)
        return new_folder_path

    def create_new_distance_folder(self):
        distance_folder = os.path.join(self.test_folder, f"distance_{int(self.distance)}")
        thermal_folder = os.path.join(distance_folder, "thermal_images")
        rgb_folder = os.path.join(distance_folder, "rgb_images")
        os.makedirs(thermal_folder, exist_ok=True)
        os.makedirs(rgb_folder, exist_ok=True)
        return distance_folder

    def callback(self, data, camera_type):
        try:
            encoding = "mono8" if camera_type == "thermal_camera" else "bgr8"
            cv_image = self.bridge.imgmsg_to_cv2(data, encoding)
            folder = "thermal_images" if camera_type == "thermal_camera" else "rgb_images"
            image_name = os.path.join(self.distance_folder, folder, f"{camera_type}_image_{self.image_count[camera_type]:04d}.png")
            cv2.imwrite(image_name, cv_image)
            rospy.loginfo(f"Saved {image_name}")
            self.image_count[camera_type] += 1
        except CvBridgeError as e:
            rospy.logerr(f"Failed to convert image: {e}")
        except Exception as e:
            rospy.logerr(f"Failed to save image: {e}")

    def move_robot(self):
        while not rospy.is_shutdown():
            x = self.distance * math.cos(math.radians(self.angle))
            y = self.distance * math.sin(math.radians(self.angle))
            orientation = self.angle_to_quaternion(self.angle + 180)  # Rotate to face the center
            call([
                "ign", "service", "-s", "/world/simple_warehouse/set_pose",
                "--reqtype", "ignition.msgs.Pose", "--reptype", "ignition.msgs.Boolean",
                "--timeout", "1000", "--req",
                f'name: "sensors", position: {{x: {x}, y: {y}, z: 0.0}}, '
                f'orientation: {{x: {orientation["x"]}, y: {orientation["y"]}, '
                f'z: {orientation["z"]}, w: {orientation["w"]}}}'
            ])
            self.angle = (self.angle + 1) % 360
            if self.angle == 0:
                self.create_video("thermal_images")
                self.create_video("rgb_images")
                self.distance += 1.0
                self.distance_folder = self.create_new_distance_folder()
                if self.distance > self.max_distance:
                    rospy.loginfo("Reached maximum distance, stopping.")
                    break
            rospy.loginfo(f"Moved robot to angle {self.angle} at distance {self.distance}")
            time.sleep(0.2)

    def create_video(self, folder_name):
        folder_path = os.path.join(self.distance_folder, folder_name)
        images = [img for img in os.listdir(folder_path) if img.endswith(".png")]
        images.sort()
        if not images:
            return
        frame = cv2.imread(os.path.join(folder_path, images[0]))
        height, width, layers = frame.shape
        video_path = os.path.join(self.distance_folder, f"{folder_name}.mp4")
        video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
        for image in images:
            video.write(cv2.imread(os.path.join(folder_path, image)))
        video.release()
        rospy.loginfo(f"Saved video {video_path}")

    def angle_to_quaternion(self, angle):
        rad = math.radians(angle)
        return {
            "x": 0.0,
            "y": 0.0,
            "z": math.sin(rad / 2),
            "w": math.cos(rad / 2)
        }

if __name__ == '__main__':
    rospy.init_node('image_listener', anonymous=True)
    listener = ImageListener()
    rospy.loginfo("Image Listener started, waiting for images...")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")