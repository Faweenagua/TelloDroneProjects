import cv2
import numpy as np


cap = cv2.VideoCapture(0)
# hsvValues = [0,0,0,179,57,255]
hsvValues = [9,0,41,179,237,143]
sensors = 3
whiteThreshold = 0.2
width, height = 480, 360
sensitivity = 3
turnWeights = [-25, -15, 0, 15, 25]
curve = 0
fSpeed = 15

def thresholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvValues[0], hsvValues[1], hsvValues[2]])
    upper = np.array([hsvValues[3], hsvValues[4], hsvValues[5]])
    mask = cv2.inRange(hsv, lower, upper)

    return mask

    
def getContours(imgThresh, img):
    cx = 0
    contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(img, contours, -1, (255, 145, 78), 7)

    if len(contours) != 0:
        biggest = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(biggest)

        cx = x + w//2
        cy = y + h//2

        # cv2.rectangle(img, (x,y), (x+w,y+h), (255, 145, 78), cv2.FILLED)
        # cv2.circle(img, (cx,cy), 10, (14,45,145), cv2.FILLED)

    return cx


def getSensorOutput(imgThresh, sensors):
    senOut = []
    imgs = np.hsplit(imgThresh, sensors)
    totalPixels = (imgThresh.shape[1]//sensors) * imgThresh.shape[0]
    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > whiteThreshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
        # cv2.imshow(str(x), im)

    return senOut

def sendCommands(senOut, cx):
    global curve

    # Translation

    lr = (cx - width//2)//sensitivity
    lr = int(np.clip(lr, -10, 10))

    if lr < 2 and lr > -2: lr = 0

    # Rotation

    if senOut == [1,0,0]: curve = turnWeights[0]
    elif senOut == [1,1,0]: curve = turnWeights[1]
    elif senOut == [0,1,0]: curve = turnWeights[2]
    elif senOut == [0,1,1]: curve = turnWeights[3]
    elif senOut == [0,0,1]: curve = turnWeights[4]


    elif senOut == [1,1,1]: curve = turnWeights[2]
    elif senOut == [1,0,1]: curve = turnWeights[2]
    elif senOut == [0,0,0]: curve = turnWeights[2]


    # me.send_rc_control(lr, fSpeed, 0, curve)



while True:
    _,img = cap.read()

    img = cv2.resize(img, (480,360))
    # img = cv2.flip(img, 0)

    imgThresh =  thresholding(img)
    cx = getContours(imgThresh, img)
    # senOut = getSensorOutput(imgThresh, sensors)
    # sendCommands(senOut, cx)


    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThresh)

    cv2.waitKey(1)