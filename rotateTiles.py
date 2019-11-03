# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:38:53 2019

@author: paolo
"""
import cv2
import numpy as np
import imutils
import glob, os

for i,file in enumerate(glob.glob("tiles/*.jpg")):
    image = cv2.imread(file) 
    height, width = image.shape[:2]
    print(height, width)
    angle = np.random.randint(1, 360)
    print(angle)
    rot_image = imutils.rotate_bound(image, angle)
    cv2.imwrite(str(file)+str(i)+'rot.jpg', rot_image)

