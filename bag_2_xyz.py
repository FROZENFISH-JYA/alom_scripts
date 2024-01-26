import rosbag
import numpy as np
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import os

def bag_to_xyz(bag_file, output_folder):
    bag = rosbag.Bag(bag_file, 'r')
    frame_count = 0

    for topic, msg, t in bag.read_messages(topics=['/ouster/points']):
        pc_data = point_cloud2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        pc_array = np.array(list(pc_data))

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save XYZ file for each frame
        xyz_file = os.path.join(output_folder, f'frame_{frame_count}.xyz')
        np.savetxt(xyz_file, pc_array, fmt='%.6f')

        frame_count += 1

    bag.close()

if __name__ == "__main__":
    bag_file_path = "./1_2023-08-24-14-42-02.bag"
    output_folder_path = "./output"
    
    bag_to_xyz(bag_file_path, output_folder_path)
    print("done")