import cv2
import numpy as np
import argparse
import math
import OpenEXR, Imath

def load_exr(in_file):
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

    img = np.zeros((size[1], size[0], 3), dtype=np.float32)
    img[:, :, 0] = red
    img[:, :, 1] = green
    img[:, :, 2] = blue

    return img

def write_exr(out_file, data):
    exr = OpenEXR.OutputFile(out_file, OpenEXR.Header(data.shape[1], data.shape[0]))
    red = data[:, :, 0]
    green = data[:, :, 1]
    blue = data[:, :, 2]
    exr.writePixels({'R': red.tostring(), 'G': green.tostring(), 'B': blue.tostring()})


def shift_img(img):
    out_img = np.zeros(img.shape, dtype=np.float32)
    y = out_img.shape[1]
    out_img[:, :y/2, :] = img[:, y/2:, :]
    out_img[:, y/2:, :] = img[:, :y/2, :]
    return out_img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str, help='Input Panorama Image')
    parser.add_argument('output_image', type=str, help='Output Panorama Image')
    args = parser.parse_args()

    img = load_exr(args.input_image)
    out_img = shift_img(img)
    write_exr(args.output_image, out_img)
