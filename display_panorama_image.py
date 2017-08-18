#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import signal
import argparse
import numpy as np
import cv2
import math
from scipy.misc import imresize

from tools import SimpleImageViewer
from panorama_image_cropper import crop_panorama_image

#
# Navigate the scene using your keyboard
#
parser = argparse.ArgumentParser()
parser.add_argument("input_image", type=str, help="Input Panorama Image")
parser.add_argument("--fov", type=float, default=60.0, help='Field of View in range [0, 180] [default: 60]')
args = parser.parse_args()

ori_img = cv2.imread(args.input_image)
img = np.array(ori_img)
img[:, :, 0] = ori_img[:, :, 2]
img[:, :, 2] = ori_img[:, :, 0]
current_img = crop_panorama_image(img, fov=args.fov)

cur_theta = 0.0
cur_phi = 0.0

stop_requested = False
img_updated = False

def key_press(key, mod):
    global cur_phi, cur_theta, stop_requested, img_updated
    if key == ord('Q') or key == ord('q'): # q/Q
        stop_requested = True
    if key == 0xFF52: # up
        if cur_phi > -80.0 / 180 * math.pi:
            cur_phi -= math.pi/12
        print 'Theta: %.4f, Phi: %.4f' % (cur_theta, cur_phi)
        img_updated = True
    if key == 0xFF53: # right
        cur_theta += math.pi/12
        cur_theta = (cur_theta + math.pi) % (2 * math.pi) - math.pi
        print 'Theta: %.4f, Phi: %.4f' % (cur_theta, cur_phi)
        img_updated = True
    if key == 0xFF51: # left
        cur_theta -= math.pi/12
        cur_theta = (cur_theta + math.pi ) % (2 * math.pi) - math.pi
        print 'Theta: %.4f, Phi: %.4f' % (cur_theta, cur_phi)
        img_updated = True
    if key == 0xFF54: # down
        if cur_phi < 80.0 / 180 * math.pi:
            cur_phi += math.pi/12
        print 'Theta: %.4f, Phi: %.4f' % (cur_theta, cur_phi)
        img_updated = True

def loop():
    global current_img, img_updated
    while True:
        if stop_requested:
            break
        
        if img_updated:
            print 'Updating...'
            img_updated = False
            current_img = crop_panorama_image(img, cur_theta/math.pi*180, cur_phi/math.pi*180, fov=args.fov)
            print 'Updated.'

        viewer.imshow(imresize(current_img, [512, 512]))

if __name__ == '__main__':
    viewer = SimpleImageViewer()
    viewer.imshow(imresize(current_img, [512, 512]))
    viewer.window.on_key_press = key_press

    print("Use arrow keys to move the agent.")
    print("Press Arrow Keys to change views.")
    print("Press Q to quit.")

    loop()

    print("Goodbye.")
