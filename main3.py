import env, sensors
import pygame
import os
import math
from djitellopy import tello
import KeyPressModule as kp
from time import sleep
import cv2

# Initialize pygame and environment
pygame.init()
environment = env.buildEnvironment((600, 1200))
environment.originalMap = environment.map.copy()
laser = sensors.LaserSensor(100, environment.originalMap, uncetainty=(0.5, 0.01))
environment.map.fill((255, 255, 255))
environment.infomap = environment.map.copy()

# --------------------- DRONE + KEYBOARD CONTROL SETUP --------------------- #
# Movement parameters
fSpeed = 600 / 10      # Forward speed (cm/s) 117
aSpeed = 360 / 10      # Angular speed (deg/s)
interval = 0.15
dInterval = fSpeed * interval
aInterval = aSpeed * interval

# Drone state
x, y = 300, 500  # Starting position on the map
a = 0            # angle in degrees
yaw = 0

# Init drone + keyboard
kp.init()
me = tello.Tello()
me.connect()
print("Battery:", me.get_battery())
# Start the camera stream
me.streamon()
# Directory to save videos
output_dir = r"C:\Users\EXCALIBUR\Desktop\drones"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Generate sequential video names
video_index = 1
video_path = os.path.join(output_dir, f"test_{video_index}.mp4")
# Define video writer (will initialize after first frame capture)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = None
fps = 30  # Frames per second



# --------------------- KEYBOARD CONTROL FUNCTION --------------------- #
def getKeyboardInput():
    global x, y, yaw, a
    lr, fb, ud, yv = 0, 0, 0, 0
    d = 0
    speed = 15
    aspeed = 50

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

    if kp.getKey("q"):
        me.land()
        sleep(3)
    if kp.getKey("e"):
        me.takeoff()

    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

# --------------------- MAIN LOOP --------------------- #
orb = cv2.ORB_create()
running = True
while running:
    pygame.time.delay(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get drone input and update position
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    x, y = vals[4], vals[5]
    robot_position = (x, y)
    # Get the video frame from the drone's camera
    frame = me.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))  # Resize frame for consistent processing

    # Apply ORB feature detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    keypoints, descriptors = orb.detectAndCompute(gray, None)  # Detect features
    frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None,color=(0, 255, 0), flags=0)
    # Draw keypoints on the frame

    # Initialize video writer on the first frame
    if video_writer is None:
        video_writer = cv2.VideoWriter(video_path, fourcc, fps, (640, 480))

    # Write the processed frame to the video file
    video_writer.write(frame_with_keypoints)

    # Display the processed video frame
    cv2.imshow("Drone Camera with ORB Features", frame_with_keypoints)
    # Set laser position and scan
    laser.position = robot_position
    sensor_data = laser.sense_obstacles()
    if sensor_data:
        environment.datastorage(sensor_data)
        environment.show_sensorData()

    # Draw map and drone
    environment.map.blit(environment.infomap, (0, 0))
    pygame.draw.circle(environment.map, environment.Blue, (int(x), int(y)), 8)
    pygame.display.update()
