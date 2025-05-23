from djitellopy import tello
import KeyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math

drone_img = cv2.imread("drone.png", cv2.IMREAD_UNCHANGED)


######## PARAMETERS ###########
fSpeed = 117 / 10  # Forward Speed in cm/s   (15cm/s)
aSpeed = 360 / 10  # Angular Speed Degrees/s  (50d/s)
interval = 0.25
dInterval = fSpeed * interval
aInterval = aSpeed * interval

###############################################

x, y = 500, 500
a = 0
yaw = 0
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
points = [(0, 0), (0, 0)]



def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global x, y, yaw, a
    d = 0
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

    if kp.getKey("q"): me.land(); sleep(3)
    if kp.getKey("e"): me.takeoff()
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]

def overlay_image(background, overlay, x, y):
    """Overlay an image (with alpha) onto a background at (x, y)."""
    h, w, _ = overlay.shape
    for i in range(h):
        for j in range(w):
            if overlay[i, j, 3] > 0:  # Check if pixel is not transparent
                background[y + i, x + j] = overlay[i, j][:3]


def drawPoints(img, points):
    for point in points:
        x, y = point
        resized_drone = cv2.resize(drone_img, (20, 20))  # Resize the drone image
        overlay_image(img, resized_drone, x - 10, y - 10)  # Center the image on the point

    last_x, last_y = points[-1]
    resized_drone = cv2.resize(drone_img, (30, 30))  # Make the last point's drone bigger
    overlay_image(img, resized_drone, last_x - 15, last_y - 15)

    # Add coordinates text
    cv2.putText(img, f'({(last_x - 500) / 100},{(last_y - 500) / 100})m',
                (last_x + 10, last_y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)




while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = np.zeros((1000, 1000, 3), np.uint8)
    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)


