import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def getContours(img):
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours,hierarchy = cv2.findContours(img, 1, 2)
    for cnt in contours:
        cv2.drawContours(img, cnt, -1, (255, 145, 78), 2)



while True:
    _,img = cap.read()

    img = cv2.resize(img, (480,360))
    # img = cv2.flip(img, 0)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1)
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    getContours(imgCanny)

    cv2.imshow("Output", img)
    cv2.imshow("Blur", imgBlur)
    cv2.imshow("Blur", imgCanny)


    cv2.waitKey(1)