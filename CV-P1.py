import cv2
import numpy as np


### Constants and assignments
corners = []
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# checkboard parameters
chessboard_size = (9, 6)

square_size = 25 #in mm

# which kind of interpolation to use
Linear = True


def calibrate_intr_camera(photos):
    for photo in photos:
       imagepoints = detect_corners(photo)
       objectpoints = world_pt()
       objpoints.extend(objectpoints)
       imgpoints.extend(imagepoints)
    return cv2.calibrateCamera(objpoints, imgpoints, chessboard_size, None, None) # make sure chessboard_size is correct, and I shouldnt use  total no. of pixles
       


def detect_corners(photo):
    img = cv2.imread(photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if not ret:
        corners = manual_corners(img)
        corners = interpolate_corners(corners)
    better_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
    
    return better_corners

def manual_corners(img):
    cv2.setMouseCallback()
    temp_img = img.copy()
    cv2.imshow("Select Four Inside Corners", temp_img)
    cv2.setMouseCallback("Select Four Inside Corners", click_event, temp_img)
        
    cv2.putText("Click on the four inside corners of the chessboard (top-left, top-right, bottom-right, bottom-left). Press ENTER when done.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return corners

def click_event(event, x, y, flags, param):
    manual_corners = []
    if event == cv2.EVENT_LBUTTONDOWN and len(manual_corners) < 4:
        manual_corners.append((x, y))
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Select Four Inside Corners", param)

        cv2.destroyWindow("Select Four Inside Corners")


def interpolate_corners(corners):
    top_left, top_right, bottom_right, bottom_left = corners[0], corners[1], corners[2], corners[3]
    #linear inrepolation
    if Linear:
        # Compute step sizes in x and y direction
        x_step = (top_right - top_left) / (chessboard_size[0])
        y_step = (bottom_left - top_left) / (chessboard_size[1])
    
        # Generate all corner points
        all_corners = []
        for i in range(chessboard_size[1]):
            for j in range(chessboard_size[0]):
                all_corners.append(top_left + j * x_step + i * y_step)
    
        return np.array(all_corners, dtype=np.float32).reshape(-1, 1, 2)
    #bilinear interpolation
    else:
        all_corners = np.zeros((chessboard_size[0] * chessboard_size[1], 2), dtype=np.float32)
        for y in range(0, chessboard_size[0]):
            for x in range(0, chessboard_size[1]):
                temp_x = x / (chessboard_size[1] - 1)
                temp_y = y / (chessboard_size[0] - 1)
                
                all_corners[x * chessboard_size[0] + y] = (
                    (1 - temp_x) * (1 - temp_y) * top_right + 
                    temp_x * (1 - temp_y) * top_left + 
                    temp_x * temp_y * bottom_left + 
                    (1 - temp_x) * temp_y * bottom_right
                )
        return all_corners
    
def world_pt():
    new_objpoints = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    new_objpoints[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size
    return new_objpoints





if __name__ == "__main__":

