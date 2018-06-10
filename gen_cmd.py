import os
import sys
import random

in_file = 'all.txt'
fin = open(in_file, 'r')

num = 8

for item in fin.readlines():
    x = item.rstrip()
    for i in range(num):
        theta = random.random() * 360 - 180
        phi = random.random() * 60 - 30
        move = -(random.random() * 0.4 + 0.4)
        cmd = 'bash script_convert_exr.sh %s %d %f %f %f' % (x, i, theta, phi, move)
        print cmd

