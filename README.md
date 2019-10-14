# Mosaic #
Mosaic is a simple program that helps you to work with large image sets and allows you to do three things with them:
1. Mosaic picture
2. Sort images by color
3. Delete duplicate images
----------

## Sorting images by color ##
This option assigns image a color name and copies it to color named directory.
To sort images use:`python mosaic.py -s [source directory] [destination directory]` where `[source directory]` is a directory with images to sort and `[destination directory]` is where you want your sorted images to be copied.
Sorting is a supporting function of this program and is based on Randall Munroe's ["Color Name Survey"](http://blog.xkcd.com/2010/05/03/color-survey-results/). There are 954 colors in total. If program can't assing image a color name the image is copied to folder `others`

## Deleting duplicate images ##

To delete duplicate images use `python -d [source directory]`. This function computes average `RGB` value for each image. If identical values were already found image is considered duplicate and then removed.

## Mosaicing image ##

This option users color sorted images so first you have to option `-s`.
To mosaic image use `python mosaic.py -m [image source] [step] [image output]`. 
`[step]` specifies size of a single mosaic square. The smaller `[step]` is the longer it takes to finish mosaicing picture

<p align="center">
<img src="https://github.com/psobczak/mosaic2/blob/master/step5.jpg" width=250 height=250/> <img src="https://github.com/psobczak/mosaic2/blob/master/step10.jpg" width=250 height=250/> <img src="https://github.com/psobczak/mosaic2/blob/master/step20.jpg" width=250 height=250/>
</p>

Here is a [set of ~18000 images](https://ufile.io/vg8sjwzh) that were used to create mosaics showed above. Feel free to download them or use your own.

## Known issues / TODOs ##
- Mosaicing and image sorting is not very efficient. Maybe add support for ~~threading~~ multiprocessing?
- For now program does not support searching for images recursively. When you sepcify `[source directory]` images can not be inside subfolders.
- Program assumes that in `[source directory]` all files are in .jpg format. For now, other formats are not supported. 
