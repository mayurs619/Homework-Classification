from heic2png import HEIC2PNG
from PIL import Image, ImageFile
import os
import shutil

# Convert each file to JPEG
def convert_to_jpg(directory, target_directory):
    heic_files = [f for f in os.listdir(directory) if f.lower().endswith('.heic')]

    # convert heic files to png and save to the same folder
    for filename in heic_files:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path.removesuffix('HEIC').removesuffix('heic') + 'png'):
            continue
        print("saving {} to png:".format(filename))
        heic_img = HEIC2PNG(file_path, quality=100)
        heic_img.save()
        print("\tsaved {} to png".format(filename))

    # convert png files to jpg and save them to the dest folder
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    png_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    for filename in png_files:
        file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(target_directory, filename.removesuffix('png') + 'jpg')
        if os.path.exists(new_file_path):
            continue

        print("saving {} to jpg:".format(filename))
        img = Image.open(file_path, mode='r')
        img.save(new_file_path)
        print("\tsaved {} to jpg".format(filename))

    # move any jpg files in src folder to dest folder
    jpg_files = [f for f in os.listdir(directory) if f.lower().endswith('.jpg')]
    jpg_files.sort()
    for filename in jpg_files:
        file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(target_directory, filename)
        if os.path.exists(new_file_path):
            continue
        shutil.copyfile(file_path, new_file_path)

if not os.path.exists('data/hw'):
    os.mkdir('data/hw')
if not os.path.exists('data/no_hw'):
    os.mkdir('data/no_hw')

for directory_name in os.listdir('data/raw_hw'):
    convert_to_jpg(os.path.join('data/raw_hw', directory_name), 'data/hw')

for directory_name in os.listdir('data/raw_no_hw'):
    convert_to_jpg(os.path.join('data/raw_no_hw', directory_name), 'data/no_hw')
