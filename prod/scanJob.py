# -*- coding: utf-8 -*-
"""
Created on 7-Feb-2020

Author : Dinesh Y

"""

# import required libraries
import os
import numpy as np
import cv2
# threshold_local will help us to get "black/white" feel to our scanned image
from skimage.filters import threshold_local 

import imutils

def scanJob(image_path_name, # input image full path and name
            bwFlag           # convert scan to black-n-white
            ):
    
    args_image = image_path_name
    args_bwflag = bwFlag

    print('[INFO] Image file/path passed: ',args_image)
    print('[INFO] Black-n-White Flag passed: ',args_bwflag)

    # -----------------------
    # STEP 1: Detect Edges
    # -----------------------
    print("[INFO] Detecting Edges")
    # read the image and keep a copy
    image = cv2.imread(args_image)
    orig = image.copy()

    # resize image to height of 500, and take ratio with original height
    # resize is done to speedup image processing without loosing 
    # any of the important information
    # take a note of the resize factor 
    # which will help us in scaling back to original size when required
    ratio = image.shape[0] / 500
    image = imutils.resize(image, height=500)

    # convert image to greyscale from RGB. This will remove any color noise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur image using gaussian blur. It helps in removing high 
    # frequency noise and it helps in finding/detecting contour in gray image
    grayBlur = cv2.GaussianBlur(gray,(5,5),0)

    # perform canny edge detection
    edged = cv2.Canny(grayBlur, 75, 200)

    # ----------------------------
    # STEP 2: Find Contours
    # ----------------------------
    print("[INFO] Finding Contours")
    # here we assumed that document in image is of the largest area 
    # and has 4 edges like a typical document. 
    # We will get area of all contours and will keep the contour 
    # with largest area having 4 edges. 

    # find the contours in the edged image, sort area wise 
    # keeping only the largest ones
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # descending sort contours area and keep top 5
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours and keep the largest contours with 4 points. 
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True) 
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        # check if approximated contour has four points. 
        # if yes then we can assume we have found our document scan
        if len(approx) == 4:
            #print("got document. Coordinates are: ",approx)
            screenCnt = approx
            break

    # ----------------------------
    # Step 3: Apply Perspective and Transform
    # ----------------------------
    print("[INFO] Applying Perspective and Transformation")

    # having obtained the 4 corner points coordinates
    # lets scale them back as per original image dimension
    pts = screenCnt.reshape(4,2) * ratio

    # we will order these corrdinates in below order. 
    # top-left, top-right, bottom-right, bottom-left
    # list to hold coordinates in above order
    rect = np.zeros((4,2), dtype="float32")

    # top left corner will have the smallest sum, 
    # bottom right corner will have the largest sum
    s = np.sum(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    #print("Top-left corner:",rect[0]," bottom-right corner:",rect[2])
    # top-right will have smallest difference
    # botton left will have largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    #print("Top-right corner:",rect[1]," bottom-left corner:",rect[3])
    #print(rect)
    (tl, tr, br, bl) = rect

    # compute width of new image
    widthA = np.sqrt((tl[0] - tr[0])**2 + (tl[1] - tr[1])**2 )
    widthB = np.sqrt((bl[0] - br[0])**2 + (bl[1] - br[1])**2 )
    maxWidth = max(int(widthA), int(widthB))
    #print("Width of document is:",maxWidth)
    # in the same way, lets compute the height of scanned image
    heightA = np.sqrt((tl[0] - bl[0])**2 + (tl[1] - bl[1])**2 )
    heightB = np.sqrt((tr[0] - br[0])**2 + (tr[1] - br[1])**2 )
    maxHeight = max(int(heightA), int(heightB))
    #print("Height of document is:",maxHeight)

    # construct a set of destination points to obtain 
    # a top-down birds-eye view of the document
    # dimension of the new image maintaining same order as above
    dst = np.array([
        [0,0],
        [maxWidth-1, 0],
        [maxWidth-1, maxHeight-1],
        [0, maxHeight-1]], dtype="float32")

    # compute the perspective transform matrix 
    M = cv2.getPerspectiveTransform(rect, dst)
    # apply the transformation matrix to ROI to obtain top-down view
    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    # ----------------------------
    # Step 4: Final Steps
    # ----------------------------
    print("[INFO] Final Processing")
    # final preparation of scanned ROI area. 
    # can convert to black/white and apply other effect here

    # convert to gray
    if args_bwflag == 'Y':
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

    return warped;


