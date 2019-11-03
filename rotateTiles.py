# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:38:53 2019

@author: paolo
"""
import cv2
import numpy as np
import imutils

for i in len(2880):
    image = cv2.imread('tile'+str(i)+'.jpg') 
    height, width = image.shape[:2]
    print(height, width)
    angle = np.random.randint(1, 360)
    print(angle)
    rot_image = imutils.rotate_bound(image, angle)
    cv2.imwrite('/rot_tiles/tile'+str(i)+'rot')

