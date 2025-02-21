import cv2
import numpy as np

corners = []
objpoints = []
imgpoints = []

def calibrate_camera(photos):
    for photo in photos:
       

def detect_corners(photo):
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None)
    if ret:
        return corners
    else:
        corners = manual_corners(img)
        return corners

def manual_corners(img):
    cv2.setMouseCallback()
    temp_img = img.copy()
    cv2.imshow("Select Four Inside Corners", temp_img)
    cv2.setMouseCallback("Select Four Inside Corners", click_event, temp_img)
        
    print("Click on the four inside corners of the chessboard (top-left, top-right, bottom-right, bottom-left). Press ENTER when done.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return corners

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN and len(manual_corners) < 4:
        manual_corners.append((x, y))
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Select Four Inside Corners", param)