from djitellopy import tello
import time
import cv2

import keyPadModule as kp

global img

kp.init()

me = tello.Tello()
me.connect()

print(me.get_battery())


me.streamon()

me.takeoff()

def getKeyboardInput():

    ud, lr, fb, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey('LEFT'): lr = -speed
    if kp.getKey('RIGHT'): lr = speed
    if kp.getKey('UP'): ud = speed
    if kp.getKey('DOWN'): ud = -speed
    if kp.getKey('KP6'): fb = speed
    if kp.getKey('KP4'): fb = -speed
    if kp.getKey('KP8'): yv = speed
    if kp.getKey('KP2'): yv = -speed

    if kp.getKey('t'): me.takeoff()
    if kp.getKey('l'): me.land(); time.sleep(3)

    if kp.getKey('c'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3);




    return [ud, lr, fb, yv]



while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[1],vals[2],vals[0],vals[3])

    img = me.get_frame_read().frame
    img = cv2.resize(img,(360,240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # if kp.getKey('c'): cv2.


    time.sleep(0.05)