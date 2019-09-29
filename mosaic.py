import os
import glob
from shutil import copy
import sys
from concurrent.futures import ThreadPoolExecutor
import fnmatch
import operator
import logging
import time
from sys import argv

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
    return np.average(image_to_average, (0, 1))


def create_folders(dest_dir):
    """Creates color-coded folders based on XKCD_COLORS color dict."""
    directory = os.path.join(dest_dir, 'colors')
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


def copy_images_to_folders(source_dir, dest_dir):
    """Sorts images in directory by color"""
    create_folders(dest_dir)

    folders = glob.glob("colors\*")
    images = glob.glob(os.path.join(source_dir, '*'))

    j = 0
    for image in images:

        img_load = cv.imread(image)
        img = average_image(img_load)
        assigned = assing_color_name(img)

        for folder in folders:
            folder_name = folder.split('\\')[1]
            image_name = image.split('\\')[1]
            if assigned['name'] == folder_name:
                dest = os.path.join(dest_dir, 'colors',
                                    folder_name, image_name)
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


def mosaic_image(image, step, output):
    """Reads image and returns new mosaiced image."""
    i = 0
    img = cv.imread(image)
    width, height = img.shape[:2]
    new_image = np.zeros((width, height, 3), np.uint8)
    step = int(step)

    # Make so image is divisible by step
    if width % step != 0 or height % step != 0:
        width = (width // step) * step
        height = (height // step) * step

    for x in range(0, width, step):
        for y in range(0, height, step):

            # Iterate over original image fragments and assign
            # each square an averaged RGB values
            square = img[x:x+step, y:y+step]
            averaged_square = average_image(square)
            square_color = assing_color_name(averaged_square)

            # Get list of color matching images
            possible_images = get_folders_content(
                os.path.join('colors', square_color['name']))

            # Get numer of possible color matching images
            number_of_possible_images = len(
                possible_images[square_color['name']])

            # If there are not matching colors go to next square
            if number_of_possible_images == 0:
                continue

            # Select random color matching image
            random_number = random.randrange(0, number_of_possible_images)
            random_matching_image = possible_images[square_color['name']
                                                    ][random_number]

            # Copy color matching image into new image
            loaded_matching_image = cv.imread(os.path.join(
                'colors', square_color['name'],  random_matching_image))
            resized_image = cv.resize(loaded_matching_image, (step, step))
            new_image[x:x+step, y:y+step] = resized_image

            # Console output
            i += 1
            print(
                f'Square {i} - {square_color["name"]} --> {random_matching_image}')
            cv.imwrite(f'{output}', new_image)
    print(f'Saved mosaiced image as {output}')


def get_folders_content(dir_name):
    """Reads a directory content and returns dict {folder_name: list_of_images}."""
    contents = {}
    for root, dirs, files in os.walk(dir_name):
        contents[root[7:]] = files
    return contents


def print_help():
    print('Mosaic - Help')
    print('-d [source directory]')
    print('-s [source directory] [destinatino directory]')
    print('-m [image source] [step] [image output]')


if __name__ == "__main__":
    if argv[1] == '-m':
        mosaic_image(argv[2], argv[3], argv[4])
    elif argv[1] == '-d':
        remove_duplicates(argv[2])
    elif argv[1] == '-s':
        copy_images_to_folders(argv[2], argv[3])
    elif argv[1] == '-h' or argv[1] == '--help':
        print_help()
