#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
import std_msgs.msg
import sensor_msgs.point_cloud2 as pc2
import numpy as np
import os
import time

def publish_xyz_files(folder_path, topic_name):
    rospy.init_node('xyz_publisher_node', anonymous=True)
    pub = rospy.Publisher(topic_name, PointCloud2, queue_size=10)

    rate = rospy.Rate(2)  # 2 Hz, adjust as needed
    frame_count = 0

    while not rospy.is_shutdown() and frame_count < 2438:  # Change the condition as needed
        xyz_file_path = os.path.join(folder_path, f'frame_{frame_count}.xyz')

        if os.path.exists(xyz_file_path):
            # Read XYZ file
            pc_array = np.loadtxt(xyz_file_path)

            # Create PointCloud2 message
            header = std_msgs.msg.Header()
            header.stamp = rospy.Time.now()
            header.frame_id = 'your_frame_id'

            pc_data = pc2.create_cloud_xyz32(header, pc_array)

            # Publish PointCloud2 message
            pub.publish(pc_data)

            rospy.loginfo(f"Published frame {frame_count} to {topic_name}")
            frame_count += 1
            rate.sleep()
        else:
            rospy.logwarn(f"Frame {frame_count} not found. Skipping.")
            frame_count += 1

if __name__ == '__main__':
    folder_path = "./output"
    topic_name = "/ouster/points"

    try:
        publish_xyz_files(folder_path, topic_name)
    except rospy.ROSInterruptException:
        pass