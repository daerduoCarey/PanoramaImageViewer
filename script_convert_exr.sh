echo 'Processing image' $1
echo 'Warping panorama image'
python convert_panorama_exr.py $1.exr $1.pano.exr --resolution_x 1000 --resolution_y 2000 --theta 90 --phi 20 --move 0.5
echo 'Cropping a regular image'
python panorama_image_cropper_exr.py $1.pano.exr $1.crop.exr --resolution_x 480 --resolution_y 640 --fov 45
echo 'Shift the panorama image'
python shift_panorama_to_left_exr.py $1.pano.exr $1.pano.exr
echo 'Outputing logint for warped panorama'
python convert_exr_to_log_intensity.py $1.pano.exr $1.pano.logint.npy $1.pano.logint.png
echo 'Outputing RGB image for warped panorama'
python ConvertEXRToJPG.py $1.pano.exr $1.pano.png
echo 'Outputing RGB image for cropped image'
python ConvertEXRToJPG.py $1.crop.exr $1.crop.png
echo 'Job Done.'
