import cv2
import numpy as np

cap = cv2.VideoCapture(0)


while True:
    _,img = cap.read()

    img = cv2.resize(img, (480,360))
    # img = cv2.flip(img, 0)


    cv2.imshow("Output", img)
    # cv2.imshow("Path", imgThresh)

    cv2.waitKey(1)