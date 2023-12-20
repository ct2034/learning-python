#!/usr/local/bin/python3

# src https://stackoverflow.com/questions/42719095/how-to-show-an-image-with-pillow-and-update-it

import numpy as np
import cv2

def sin2d(x,y):
    """2-d sine function to plot"""
    return np.sin(x) + np.cos(y)

def getFrame(p):
    """Generate next frame of simulation as numpy array"""

    # Create data on first call only
    if getFrame.z is None:
        getFrame.z = np.zeros((h, w,3), np.uint8)
        getFrame.z[p[1],p[0],:] = 255
    
    # decay existing data
    getFrame.z = getFrame.z * 0.99

    # random path
    prev_p = p
    dir = np.random.randint(0, 4)
    l = np.random.randint(0, 50)
    if dir == 0:
        p = (prev_p[0]+l, prev_p[1])
    elif dir == 1:
        p = (prev_p[0]-l, prev_p[1])
    elif dir == 2:
        p = (prev_p[0], prev_p[1]+l)
    else:
        p = (prev_p[0], prev_p[1]-l)

    # check boundaries
    if p[0] >= h:
        p = (h-1, p[1])
    elif p[0] < 0:
        p = (0, p[1])
    if p[1] >= w:
        p = (p[0], w-1)
    elif p[1] < 0:
        p = (p[0], 0)

    # draw line from previous point to current point
    cv2.line(getFrame.z, prev_p, p, (255,255,255), 1)

    return getFrame.z, p

# Frame size
w, h = 1920, 1080
p = (w//2, h//2)

getFrame.z = None

# remove the following two lines for not full screen
cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('image',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

while True:
       
    # Get a numpy array to display from the simulation
    npimage, p = getFrame(p)

    cv2.imshow('image', npimage)
    cv2.waitKey(1)