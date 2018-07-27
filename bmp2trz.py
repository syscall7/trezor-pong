#! /usr/bin/env python
# ------------------------------------------------------------------------------
# File: bmp2trz.py
# Author: Anthony DeRosa
# Date: July 2018
#
# Purpose: Convert a Windows *.bmp file to a C array for displaying on Trezor
#          The output C array can be placed in trezor-mcu/gen/bitmaps.c.
#          The input bitmap file should be in 24-bit mode, and you should scale
#          the file to something less than 128x64 before running this utility.
#          You can scale the image with an image editor like gimp or on the
#          command line as follows:
#               convert title.bmp -resize 128x64 title_resized.bmp
#
# Usage: ./bmp2trz.py <input.bmp> <output.c>
# ------------------------------------------------------------------------------
import struct
import sys

def error(msg):
    sys.stderr.write(msg+"\n")
    sys.exit(1)

def bmp2trz(ipath, opath):

    with open(ipath, 'rb') as inf:
        bmp = inf.read()

    # verify the magic
    magic = struct.unpack("<H", bmp[0:2])[0]
    if magic != 0x4d42:
        error("File format not recognized")

    # read out some info from the BMP header
    pixstart = struct.unpack("<I", bmp[10:14])[0]
    width = struct.unpack("<I", bmp[18:22])[0]
    height = struct.unpack("<I", bmp[22:26])[0]
    pixels = bmp[pixstart:]

    # sanity check to see if there is any unexpected padding
    if len(pixels) != (height*width*3):
        error("Pixel data not in unexpected format")

    # keep track of the output bytes
    outbytes = []

    # for each row in the bitmap, starting from the bottom left corner
    for row in zip(*[pixels[i::(width*3)] for i in range(width*3)]):
        # initialize an empty row that is compressed down to one bit per pixel
        trzBytes = [0]*(width/8)
        # for each pixel, from left to right
        for j, pixel in enumerate(zip(*[row[i::3] for i in range(3)])):
            # flatten the green pixel to white or block
            bit = 0 if ord(pixel[1]) < 128 else 1
            # store the bits from left to right starting with LSB
            trzBytes[j>>3] |= (bit << (7 - (j % 8)))

        outbytes.extend(trzBytes)

    # write out as a C array
    with open(opath, 'w') as outf:
        outf.write("const uint8_t bmp_data[] = {\n")
        for j in range(height):
            for i in range(width/8):
                outf.write("0x%02x, " % outbytes[(height - 1 - j)*(width >> 3) + i])
            outf.write("\n");
        outf.write("};")


if __name__ == "__main__":
    bmp2trz(sys.argv[1], sys.argv[2])
