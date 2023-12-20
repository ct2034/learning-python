#!/usr/local/bin/python3

# src https://stackoverflow.com/questions/42719095/how-to-show-an-image-with-pillow-and-update-it

import numpy as np
import cv2
import time


def initFrame(h, w):
    """Initialize the simulation frame"""
    return np.zeros((h, w, 3), np.uint8)


def dist(a, b):
    """Distance between two points"""
    return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def getNextFrame(old_frame, particles, h, w):
    """Generate next frame of simulation as numpy array"""
    mid = (w//2, h//2)
    
    # decay existing data
    old_frame = old_frame * 0.9
    
    # random path
    for i_p, p in enumerate(particles):
        prev_p = p
        offcenter = dist(p, mid)
        l = max(5, int(offcenter/40))
        l = float(np.random.randint(0, l))
        dir = np.random.random() * 2. * np.pi
        p = (
            int(np.round(p[0] + l * np.cos(dir))),
            int(np.round(p[1] + l * np.sin(dir)))
        )

        # check boundaries
        if p[0] >= w:
            p = (w-1, p[1])
        elif p[0] < 0:
            p = (0, p[1])
        if p[1] >= h:
            p = (p[0], h-1)
        elif p[1] < 0:
            p = (p[0], 0)

        col = (
            int(255. * (1. - (offcenter / (w/2)))),
            int(255. * (offcenter / (w/2))),
            128
        )

        # draw line from previous point to current point
        cv2.line(old_frame, prev_p, p, col, 1)

        # update particle
        particles[i_p] = p

    return old_frame, particles

def initParticles(h, w, n):
    """Initialize the particles"""
    p = []
    for i in range(n):
        p.append((np.random.randint(0, w), np.random.randint(0, h)))
    return p

def main():
    # Frame size
    w, h = 1920, 1080
    p = (w//2, h//2)

    # remove the following two lines for not full screen
    cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('image',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


    # to screen
    fps_display_interval = 5  # seconds
    last_fps_display_time = 0

    npimage = initFrame(h, w)
    particles = initParticles(h, w, 1000)

    while True:
        start = time.time()   
        # Get a numpy array to display from the simulation
        npimage, particles = getNextFrame(npimage, particles, h, w)
        # getFrame.z = npimage

        cv2.imshow('image', npimage)
        cv2.waitKey(1)

        # print fps
        if last_fps_display_time < time.time() - fps_display_interval:
            print('FPS {:.1f}'.format(1 / (time.time() - start)))
            last_fps_display_time = time.time()

if __name__ == '__main__':
    main()