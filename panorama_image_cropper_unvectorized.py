import cv2
import numpy as np
import argparse
import math

def crop_panorama_image(img, theta=0.0, phi=0.0, res_x=256, res_y=256, fov=60.0, debug=False):
    img_x = img.shape[0]
    img_y = img.shape[1]

    theta = theta / 180 * math.pi
    phi = phi / 180 * math.pi

    fov_x = fov
    aspect_ratio = res_y * 1.0 / res_x
    half_len_x = math.tan(fov_x / 180 * math.pi / 2)
    half_len_y = aspect_ratio * half_len_x

    pixel_len_x = 2 * half_len_x / res_x
    pixel_len_y = 2 * half_len_y / res_y

    map_x = np.zeros((res_x, res_y), dtype=np.float32)
    map_y = np.zeros((res_x, res_y), dtype=np.float32)

    axis_y = math.cos(theta)
    axis_z = math.sin(theta)
    axis_x = 0

    # phi rotation matrix
    cos_phi = math.cos(phi)
    sin_phi = -math.sin(phi)
    rot_mat = np.array([[cos_phi + axis_x**2 * (1 - cos_phi), \
            axis_x * axis_y * (1 - cos_phi) - axis_z * sin_phi, \
            axis_x * axis_z * (1 - cos_phi) + axis_y * sin_phi], \
            [axis_y * axis_x * (1 - cos_phi) + axis_z * sin_phi, \
            cos_phi + axis_y**2 * (1 - cos_phi), \
            axis_y * axis_z * (1 - cos_phi) - axis_x * sin_phi], \
            [axis_z * axis_x * (1 - cos_phi) - axis_y * sin_phi, \
            axis_z * axis_y * (1 - cos_phi) + axis_x * sin_phi, \
            cos_phi + axis_z**2 * (1 - cos_phi)]], dtype=np.float32)

    for x in range(res_x):
        for y in range(res_y):
            ori_x_loc = x * pixel_len_x + pixel_len_x / 2 - half_len_x
            ori_y_loc = y * pixel_len_y + pixel_len_y / 2 - half_len_y
            ori_z_loc = -1.0

            y_loc1 = math.cos(theta) * ori_y_loc - math.sin(theta) * ori_z_loc
            z_loc1 = math.sin(theta) * ori_y_loc + math.cos(theta) * ori_z_loc
            x_loc1 = ori_x_loc

            apply_phi_rot = rot_mat.dot(np.array([x_loc1, y_loc1, z_loc1]))

            x_loc = apply_phi_rot[0]
            y_loc = apply_phi_rot[1]
            z_loc = apply_phi_rot[2]

            cur_len = math.sqrt(x_loc**2 + y_loc**2 + z_loc**2)

            x_loc = x_loc / cur_len
            y_loc = y_loc / cur_len
            z_loc = z_loc / cur_len

            cur_phi = np.arcsin(x_loc)
            cur_theta = np.arctan2(y_loc, -z_loc)

            map_x[x, y] = (cur_phi + math.pi/2) / math.pi * img_x
            map_y[x, y] = cur_theta % (2 * math.pi) / (2 * math.pi) * img_y

    if debug:
        for x in range(res_x):
            for y in range(res_y):
                print '(%.2f, %.2f)\t' % (map_x[x, y], map_y[x, y]),
            print

    return cv2.remap(img, map_y, map_x, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_image', type=str, help='Input Panorama Image')
    parser.add_argument('output_image', type=str, help='Output Panorama Image')
    parser.add_argument('--theta', type=float, default=0.0, help='Theta angle (yaw) in range [-180, 180] degrees [default: 0.0]')
    parser.add_argument('--phi', type=float, default=0.0, help='Phi angle (pitch) in range [-90, 90) degrees [default: 0.0]')
    parser.add_argument('--resolution_x', type=int, default=256, help='Resolution of the output image width [default: 256]')
    parser.add_argument('--resolution_y', type=int, default=256, help='Resolution of the output image height [default: 256]')
    parser.add_argument('--fov', type=float, default=60.0, help='Field of View for image height in range [0, 180] degrees [default: 60.0]')
    parser.add_argument('--debug', type=bool, default=False, help='Debug mode')
    args = parser.parse_args()

    img = cv2.imread(args.input_image)
    in_img = np.concatenate((img, img), axis=1)
    out_img = crop_panorama_image(img, theta=args.theta, phi=args.phi, res_x=args.resolution_x, \
            res_y=args.resolution_y, fov=args.fov, debug=args.debug)
    cv2.imwrite(args.output_image, out_img)
