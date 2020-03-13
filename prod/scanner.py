# -*- coding: utf-8 -*-
"""
Created on 7-Feb-2020

Author : Dinesh Y

"""
import os
import cv2
from scanJob import *
import argparse

# -----------------------
# parse input parameters
# -----------------------

# 1. input scanned photograph 
# 2. flag if need B/W output
image_path_name = "card_scan.png"
bwFlag = "N"

try:
    scan = scanJob(image_path_name=image_path_name, bwFlag=bwFlag  )

    # show the scanned area
    #origImage = cv2.imread(image_path_name)
    #cv2.imshow("Original",origImage)
    cv2.imshow("Scanned",scan)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

except Exception as e: 
    print(e)
    outText=e



