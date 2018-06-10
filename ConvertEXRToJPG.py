#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import numpy

import OpenEXR
import Imath
import Image


# refer: 
# * [OpenEXR interfacing with other packages][1]
# * [Converting Linear EXR to sRGB JPEG with Python?][2]
#
# [1]: http://excamera.com/articles/26/doc/intro.html
# [2]: http://tech-artists.org/forum/showthread.php?2339-Converting-Linear-EXR-to-sRGB-JPEG-with-Python
#

def ConvertEXRToJPG(exrfile, jpgfile):
    File = OpenEXR.InputFile(exrfile)
    PixType = Imath.PixelType(Imath.PixelType.FLOAT)
    DW = File.header()['dataWindow']
    Size = (DW.max.x - DW.min.x + 1, DW.max.y - DW.min.y + 1)

    rgb = [numpy.fromstring(File.channel(c, PixType), dtype=numpy.float32) for c in 'RGB']
    for i in range(3):
        rgb[i] = numpy.where(rgb[i]<=0.0031308,
                (rgb[i]*12.92)*255.0,
                (1.055*(rgb[i]**(1.0/2.4))-0.055) * 255.0)
    
    rgb8 = [Image.frombytes("F", Size, c.tostring()).convert("L") for c in rgb]
    #rgb8 = [Image.fromarray(c.astype(int)) for c in rgb]
    Image.merge("RGB", rgb8).save(jpgfile, "JPEG", quality=95)


def EncodeToSRGB(v):
    if (v <= 0.0031308):
        return (v * 12.92) * 255.0
    else:
        return (1.055*(v**(1.0/2.4))-0.055) * 255.0


def main(argv=sys.argv[:]):
    # print 'from %s to %s' % (argv[1], argv[2])
    ConvertEXRToJPG(argv[1], argv[2])
    return 0


if __name__ == '__main__':
    sys.exit(main())
