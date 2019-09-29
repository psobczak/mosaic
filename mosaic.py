import os
import glob
from shutil import copy
import sys
from concurrent.futures import ThreadPoolExecutor
import fnmatch
import operator
import logging
import time

from timeit import default_timer
import random
import cv2 as cv
import numpy as np
from matplotlib.colors import XKCD_COLORS, rgb2hex
from webcolors import hex_to_name, hex_to_rgb
from resizeimage import resizeimage


IMAGES = glob.glob("images\*")


def assing_color_name(averaged_color):
    """User XKCD_COLORS colors dict to assign name for specified color."""
    for color, value in XKCD_COLORS.items():
        rgb_from_hex = hex_to_rgb(value)
        if imgs_close_enough(averaged_color, rgb_from_hex, 25):
            return {
                'name': color[5:],
                'rgb': averaged_color
            }
    return {
        'name': 'other',
        'rgb': averaged_color
    }


def average_image(image_to_average):
    """Averages image to single RGB value."""
    rgb = []
    if len(image_to_average) > 3:
        average = np.average(image_to_average, (0, 1))
        rgb.append(average[2])
        rgb.append(average[1])
        rgb.append(average[0])
    else:
        rgb = np.average(image_to_average)
    return rgb


def create_folders():
    """Creates color-coded folders based on XKCD_COLORS color dict."""
    directory = "colors"
    os.makedirs(directory, exist_ok=True)
    for color in XKCD_COLORS:
        if not os.path.exists(color):
            os.makedirs(os.path.join(directory, color[5:]), exist_ok=True)
    os.makedirs(os.path.join(directory, 'other'), exist_ok=True)
    print("Creating folders ...")


def imgs_close_enough(imageA, imageB, diff):
    """Checks if imageA is colorwise close enough to imageB
    and returns boolean."""
    return np.allclose(imageA, imageB, atol=diff)


def copy_images_to_folders():
    create_folders()
    j = 0
    for image in IMAGES:

        img_load = cv.imread(image)
        img = average_image(img_load)
        assigned = assing_color_name(img)

        for folder in glob.glob("colors\*"):
            folder_name = folder.split('\\')[1]
            image_name = image.split('\\')[1]
            if assigned['name'] == folder_name:
                dest = os.path.join('colors', folder_name, image_name)
                copy(image, dest)
                print(f"""{j}. Copied {image_name} to {folder_name}""")
                j += 1


def remove_duplicates(directory_path):
    """Removes duplicate images from directory."""
    print(f'Indexing images...')
    images = glob.glob(os.path.join(directory_path, '*.jpg'))
    set_img = set()
    for image in images:
        img = tuple(average_image(cv.imread(image)))
        if img not in set_img:
            set_img.add(img)
        else:
            os.remove(image)
            print(f'Removing {image} ...')


def mosaic_image(image, step):
    i = 0
    img = cv.imread(image)
    width, height = img.shape[:2]
    new_image = np.zeros((width, height, 3), np.uint8)

    if width % step is not 0 or height % step is not 0:
        width = (width // step) * step
        height = (height // step) * step

    for x in range(0, width, step):
        for y in range(0, height, step):

            # Iterate over original image fragments and assign
            # each square an averaged RGB values
            square = img[x:x+step, y:y+step]
            averaged_square = average_image(square)
            square_color = assing_color_name(averaged_square)

            # {'name': 'camouflage green', 'rgb': [71.38, 87.9925, 28.115]} - square_color
            # Get list of color matching images
            possible_images = get_folders_content(
                os.path.join('colors', square_color['name']))

            # if not possible_images[square_color['name']]:
            #     continue

            number_of_possible_images = len(
                possible_images[square_color['name']])
            if number_of_possible_images == 0:
                # TODO: If True add solid color square instead of new image
                continue

            random_number = random.randrange(0, number_of_possible_images)
            random_matching_image = possible_images[square_color['name']
                                                    ][random_number]

            # Copy color images into new image
            loaded_matching_image = cv.imread(os.path.join(
                'colors', square_color['name'],  random_matching_image))
            resized_image = cv.resize(loaded_matching_image, (step, step))
            # cv.imshow('sad', resized_image)

            # cv.waitKey(0)
            new_image[x:x+step, y:y+step] = resized_image
            i += 1
            print(
                f'Square {i} - {square_color["name"]} --> {random_matching_image}')

    return new_image

    # print(square)


def get_folders_content(dir_name):
    contents = {}
    for root, dirs, files in os.walk(dir_name):
        contents[root[7:]] = files
        # print(root[7:], len(files))
    return contents


# print(get_folders_content('colors\\red'))

# a = get_folders_content()
# sorte = sorted(a.items(), key=lambda k: k[1], reverse=True)
# for d in sorte:
#     print(d[0], d[1])
# # print(sorte)
# ja = cv.imread('kasia.jpg')
# print(ja.shape[:2])


start = default_timer()
a = mosaic_image('ja.jpg', 5)
end = default_timer()
print((end - start) / 60)
cv.imwrite(f'{str(time.time())[:10]}_mosaiced.jpg', a)
cv.imshow('asd ', a)
cv.waitKey(0)


# if __name__ == "__main__":
#     # remove_duplicates('images')
#     copy_images_to_folders()
