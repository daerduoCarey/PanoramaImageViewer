import OpenEXR, Imath
import numpy as np
import os, sys
from scipy.misc import imsave
import matplotlib.pyplot as plt

in_file = sys.argv[1]
log_int_file = in_file.replace('.exr', '.logint.npy')
log_int_visu_file = in_file.replace('.exr', '.logint.png')

pt = Imath.PixelType(Imath.PixelType.FLOAT)
golden = OpenEXR.InputFile(in_file)
dw = golden.header()['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

redstr = golden.channel('R', pt)
red = np.fromstring(redstr, dtype = np.float32)
red.shape = (size[1], size[0]) # Numpy arrays are (row, col)

greenstr = golden.channel('G', pt)
green = np.fromstring(greenstr, dtype = np.float32)
green.shape = (size[1], size[0]) # Numpy arrays are (row, col)

bluestr = golden.channel('B', pt)
blue = np.fromstring(bluestr, dtype = np.float32)
blue.shape = (size[1], size[0]) # Numpy arrays are (row, col)

luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
luminance[luminance < 1] = 1
log_intensity = np.log10(luminance)

plt.imsave(log_int_visu_file, log_intensity, cmap='jet')
np.save(log_int_file, log_intensity)
