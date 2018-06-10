echo 'Processing image' $1 $2
echo $3 $4 $5 > ../warping_params/$1_$2.txt
python convert_panorama_exr.py ../ori_exr/$1.exr ../warped_exr/$1_$2.exr --resolution_x 128 --resolution_y 256 --theta $3 --phi $4 --move $5
python panorama_image_cropper_exr.py ../warped_exr/$1_$2.exr ../cropped_exr/$1_$2.exr --resolution_x 192 --resolution_y 256 --fov 45
python shift_panorama_to_left_exr.py ../warped_exr/$1_$2.exr ../warped_exr/$1_$2.exr
python convert_exr_to_log_intensity.py ../warped_exr/$1_$2.exr ../warped_logint_npy/$1_$2.npy ../warped_logint_png/$1_$2.png
convert ../warped_exr/$1_$2.exr -auto-gamma ../warped_rgb/$1_$2.png
convert ../cropped_exr/$1_$2.exr -auto-gamma ../cropped_rgb/$1_$2.png
