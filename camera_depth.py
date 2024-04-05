import cv2
import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt

pipe = rs.pipeline()
config = rs.config()
config.enable_device_from_file('image_cam.jpg')
profile = pipe.start(config)

for x in range(5):
  pipe.wait_for_frames()
  
# Store next frameset for later processing:
frameset = pipe.wait_for_frames()
color_frame = frameset.get_color_frame()
depth_frame = frameset.get_depth_frame()

# Cleanup:
pipe.stop()
colorizer = rs.colorizer()
colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())
plt.imshow(colorized_depth)