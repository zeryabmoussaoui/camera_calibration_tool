# Author : Zeryab Moussaoui (zeryab.moussaoui@gmail.com)
# Description : Compute calibration matrix from (web)camera
# Inspired from : https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
# Version : 1.0

import numpy as np
import cv2
import yaml

# Parameters
#TODO : Read from file
n_row=6 
n_col=7
n_min_img = 10 # img needed for calibration
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # termination criteria
corner_accuracy = (11,11)
result_file = "./calibration.yaml"

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(n_row-1,n_col-1,0)
objp = np.zeros((n_row*n_col,3), np.float32)
objp[:,:2] = np.mgrid[0:n_row,0:n_col].T.reshape(-1,2)

# Intialize camera and window
camera = cv2.VideoCapture(0) #Supposed to be the only camera
if not camera.isOpened():
    print("Camera not found!")
    quit()
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))  
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
cv2.namedWindow("Calibration")


# Usage
def usage():
    print("Press on displayed window : \n")
    print("[space]     : take picture")
    print("[c]         : compute calibration")
    print("[r]         : reset program")
    print("[ESC]    : quit")

usage()
Initialization = True

while True:    
    if Initialization:
        print("Initialize data structures ..")
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        n_img = 0
        Initialization = False
        tot_error=0
    
    # Read from camera and display on windows
    ret, img = camera.read()
    cv2.imshow("Calibration", img)
    if not ret:
        print("Cannot read camera frame, exit from program!")
        camera.release()        
        cv2.destroyAllWindows()
        break
    
    # Wait for instruction 
    k = cv2.waitKey(50) 
   
    # SPACE pressed to take picture
    if k%256 == 32:   
        print("Adding image for calibration...")
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(imgGray, (n_row,n_col),None)

        # If found, add object points, image points (after refining them)
        if not ret:
            print("Cannot found Chessboard corners!")
            
        else:
            print("Chessboard corners successfully found.")
            objpoints.append(objp)
            n_img +=1
            corners2 = cv2.cornerSubPix(imgGray,corners,corner_accuracy,(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            imgAugmnt = cv2.drawChessboardCorners(img, (n_row,n_col), corners2,ret)
            cv2.imshow('Calibration',imgAugmnt) 
            cv2.waitKey(500)        
                
    # "c" pressed to compute calibration        
    elif k%256 == 99:        
        if n_img <= n_min_img:
            print("Only ", n_img , " captured, ",  " at least ", n_min_img , " images are needed")
        
        else:
            print("Computing calibration ...")
            ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (width,height),None,None)
            
            if not ret:
                print("Cannot compute calibration!")
            
            else:
                print("Camera calibration successfully computed")
                # Compute reprojection errors
                for i in range(len(objpoints)):
                   imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
                   error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
                   tot_error += error
                print("Camera matrix: ", mtx)
                print("Distortion coeffs: ", dist)
                print("Total error: ", tot_error)
                print("Mean error: ", np.mean(error))
                
                # Saving calibration matrix
                print("Saving camera matrix .. in ",result_file)
                data={"camera_matrix": mtx.tolist(), "dist_coeff": dist.tolist()}
                with open(result_file, "w") as f:
                    yaml.dump(data, f, default_flow_style=False)
                
    # ESC pressed to quit
    elif k%256 == 27:
            print("Escape hit, closing...")
            camera.release()        
            cv2.destroyAllWindows()
            break
    # "r" pressed to reset
    elif k%256 ==114: 
         print("Reset program...")
         Initialization = True
        
            
        
        
        
        
