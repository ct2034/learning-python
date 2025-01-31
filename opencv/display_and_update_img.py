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


def getBaseField(h, w, t):
    """Generate a base field of directions [0, 2pi]"""
    directions = -(
        np.sin(33. * np.arange(w) / w + t) +
        np.sin(42. * np.arange(h) / h + t)[:, None] +
        np.cos(101. * np.arange(w) / w + t) +
        np.sin(83. * np.arange(h) / h + t)[:, None] +
        np.cos(53. * np.arange(w) / w + t) +
        np.cos(69. * np.arange(h) / h + t)[:, None]
    )

    # normalize to [0, 1]
    mi = np.min(directions)
    ma = np.max(directions)
    directions = (directions - mi) / (ma - mi)
    return directions


def getNextFrame(i, old_frame, particles, directions, dirField, h, w):
    """Generate next frame of simulation as numpy array"""
    mid = (w//2, h//2)
    
    # decay existing data
    old_frame = old_frame * 0.98
    old_frame = cv2.GaussianBlur(old_frame, (7, 7), 0.8)

    prev_p = particles.copy()
    offcenter = np.linalg.norm(particles - mid, axis=1)

    for i_p, p in enumerate(particles):
        l = np.random.normal(0, 1) + 6.
        fielddir = dirField[p[1], p[0]] * 4. * \
            np.pi + np.random.normal(0, 0.08)
        fielddir = fielddir % (2. * np.pi)

        d_dir = directions[i_p] - fielddir
        while d_dir > np.pi:
            d_dir -= 2. * np.pi
        while d_dir < -np.pi:
            d_dir += 2. * np.pi
        dir = directions[i_p] - d_dir * 0.06

        p = (
            int(p[0] + l * np.cos(dir)),
            int(p[1] + l * np.sin(dir))
        )

        # wrap around
        wrapped = False
        if p[0] >= w:
            p = (p[0] - w, p[1])
            wrapped = True
        if p[0] < 0:
            p = (p[0] + w, p[1])
            wrapped = True
        if p[1] >= h:
            p = (p[0], p[1] - h)
            wrapped = True
        if p[1] < 0:
            p = (p[0], p[1] + h)
            wrapped = True

        t = i + i_p / 4.

        offcent = (offcenter[i_p] / (dist(mid, (0, 0))))
        central = (1. - offcent) ** 2
        brightness = 0.5 + 0.5 * central

        col = (
            brightness * (.5 + .5 * np.cos(t / 187.) * central),
            brightness * (.5 + .5 * np.cos(t / 87.) * offcent),
            brightness * (.5 + .5 * np.sin(t / 101.))
        )
        # col = (
        #     (1. * offcent),
        #     (1. * (p[0] / w)),
        #     (1. * (p[1] / h))
        # )
                
        # if i % 200 == 0:
        #     print(col)

        # draw line from previous point to current point
        if not wrapped:
            # cv2.line(old_frame, prev_p[i_p], p, (0, 0, 0), 2)
            cv2.line(old_frame, prev_p[i_p], p, col, 1)

        # update particle
        particles[i_p] = p
        directions[i_p] = dir

    return old_frame, particles, directions

def initParticles(h, w, n):
    """Initialize the particles"""
    p = []
    for i in range(n):
        p.append((np.random.randint(0, w), np.random.randint(0, h)))
    return np.array(p)

def initDirections(n):
    """Initialize the particles"""
    return np.random.rand(n) * 2. * np.pi

def main():
    # Frame size
    w, h = 1920, 1080
    n = 800

    # remove the following two lines for not full screen
    cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('image',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


    # to screen
    fps_display_interval = 5  # seconds
    last_fps_display_time = 0

    npimage = initFrame(h, w)
    particles = initParticles(h, w, n)
    directions = initDirections(n)

    i = 0
    while True:
        start = time.time()   
        # Get a numpy array to display from the simulation
        if i % 10 == 0:
            dirField = getBaseField(h, w, t = i / 100.)
        npimage, particles, directions = getNextFrame(
            i, npimage, particles, directions, dirField, h, w)
        i += 1

        cv2.imshow('image', npimage)
        cv2.waitKey(1)

        # print fps
        if last_fps_display_time < time.time() - fps_display_interval:
            print('FPS {:.1f}'.format(1 / (time.time() - start)))
            last_fps_display_time = time.time()

if __name__ == '__main__':
    main()