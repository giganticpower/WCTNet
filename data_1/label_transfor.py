from PIL import Image
import os

# path to directory containing tif images
tif_dir = '/data_1/train/gt'

# create directory for saving png images
if not os.path.exists('/data_1/train/Label_ori'):
    os.makedirs('/data_1/train/Label_ori')

# loop through all tif images in directory and convert to png
for file_name in os.listdir(tif_dir):
    if file_name.endswith('.tif'):
        # open tif image
        with Image.open(os.path.join(tif_dir, file_name)) as im:
            # convert to binary image
            binary_im = im.convert('1')
            # save as png image
            png_file_name = file_name[:-4] + '_mask.png'
            png_path = os.path.join('/data_1/train/Label_ori', png_file_name)
            binary_im.save(png_path)
