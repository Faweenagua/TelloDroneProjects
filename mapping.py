from djitellopy import tello
import time
import cv2
import numpy as np
import math

import keyPadModule as kp

global img


####### PARAMETERS ##########
forwardSpeed = 117/10  #forward speed in cm/s (15cm/s)
angularSpeed = 360/10 #Angular speed Degree/s (50degree/s)

interval = 0.25

distanceInterval = forwardSpeed *interval
angularInterval = angularSpeed*interval

##############################
x, y = 500, 500;
a = 0;
yaw = 0
points = []

kp.init()

me = tello.Tello()
me.connect()

print(me.get_battery())


me.streamon()

me.takeoff()

def getKeyboardInput():

    ud, lr, fb, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    d = 0
    global yaw,x,y,a


    if kp.getKey('LEFT'): 
        lr = -speed
        d = distanceInterval
        a = -180
    if kp.getKey('RIGHT'): 
        lr = speed
        d = -distanceInterval
        a = 180
    if kp.getKey('UP'): 
        fb = speed
        d = distanceInterval
        a = 270
    if kp.getKey('DOWN'): 
        fb = -speed
        d = -distanceInterval
        a = -90
    if kp.getKey('KP2'): ud = speed
    if kp.getKey('KP8'): ud = -speed
    
    if kp.getKey('KP4'): 
        yv = aspeed
        yaw += angularInterval

    if kp.getKey('KP6'): 
        yv = -aspeed
        yaw -= angularInterval

    if kp.getKey('t'): me.takeoff()
    if kp.getKey('l'): me.land(); time.sleep(3)

    if kp.getKey('c'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3);
    
    time.sleep(interval)

    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))





    return [ud, lr, fb, yv, x, y]


def drawPoint(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 10, (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]-500)/100}, {(points[-1][1]-500)/100})m', (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[1],vals[2],vals[0],vals[3])
    print(me.get_height())


    img = np.zeros((1000, 1000, 3), np.uint8)

    points.append((vals[4], vals[5]))
    drawPoint(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)