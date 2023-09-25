from djitellopy import tello
from time import sleep
import keyPadModule as kp

kp.init()

me = tello.Tello()
me.connect()

print(me.get_battery())

me.takeoff()

def getKeyboardInput():

    ud, lr, fb, yv = 0
    speed = 50

    if kp.getKey('LEFT'): lr = -speed
    if kp.getKey('RIGHT'): lr = speed
    if kp.getKey('UP'): ud = speed
    if kp.getKey('DOWN'): ud = -speed
    if kp.getKey('6'): fb = speed
    if kp.getKey('4'): fb = -speed
    if kp.getKey('8'): yv = speed
    if kp.getKey('2'): yv = -speed

    if kp.getKey('t'): me.takeoff()
    if kp.getKey('l'): me.land()



    return [ud, lr, fb, yv]



while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[1],vals[2],vals[0],vals[3])
    sleep(0.05)

kp.getKey("s");