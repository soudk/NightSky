# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 21:38:53 2019

@author: paolo
"""
import cv2
import numpy as np
import imutils
import glob, os
import scipy.misc

if os.path.exists('./rot-tiles/') == False:
    os.makedirs('rot-tiles/')
else:
    pass
for i in range(20):
    for i,file in enumerate(glob.glob("tiles/*.jpg")):

        #print(file)
        split=file.split("_")
        if ("RA" in file) or ("DEC" in file):
        	#print(file)
        	#print(file)
        	continue
        #print(split[1])
        image = cv2.imread(file) 
        height, width = image.shape[:2]
        #print(height, width)
        angle = np.random.randint(1, 360)
        side_length_factor = np.random.random()*3 + 1
        #print(angle)
        w= int(width*side_length_factor)
        h=int(height*side_length_factor)
        rot_image = imutils.rotate(image, angle)
        #rot_image = imutils.resize(rot_image, width = w, height = h)
        #rot_image=np.reshape(rot_image, (w, h))
        scipy.misc.toimage(rot_image, cmin=0.0, cmax=1.0).save('rot-tiles/' + str(split[1]) + '_'+ 'rot' +'_' +str(angle) + '.jpg')

	#cv2.imwrite('rot_tiles/' +str(file) + str(i) + 'rot' + str(angle) + '.jpg', rot_image)

