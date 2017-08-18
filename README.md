## Panorama Image Viewer and Cropper

Author: Kaichun Mo

Webpage: [http://www.cs.stanford.edu/~kaichun/](http://www.cs.stanford.edu/~kaichun/)

### Usage

To view the panorama image, please use the following code.

    python display_panorama_image.py sample_img.jpg --fov 60.0

Use arrow keys to navigate through the image space.

To generate the download the cropped images, please run this.

    python panorama_image_cropper.py [input_image] [output_image] \
        --theta [theta of the crop center] --phi [phi of the crop center] \
        --resolution_x [res_x] --resolution_y [res_y] --fov [fov] \

### License

MIT
