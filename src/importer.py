#!/usr/bin/env python3
import os
import sys
from pprint import pformat
from PIL import Image

# Make an importer that will be able to add a black and white animation or image made on Piskel or some other pixel art editor.
# Then play with them programatically

TEMPLATE_STATIC = """\
class %s(Static):
    def __init__(self):
        self.center = [0,0]
        self.frame = %s
"""

TEMPLATE_ANIM = """\
class %s(Anim):
    def __init__(self):
        self.tick = 0
        self.reset = %s
        self.tick_rate = 1
        self.center = [0,0]
        self.frames = %s
"""


def import_image(name, target):
    bm = [] # binary matrix
    img = Image.open(target)
    pixels = img.load()

    for i in range(0, img.height):
        row = []
        for j in range(0, img.width):
            if pixels[j,i] == (0,0,0,255):
               row.append(1)
            else:
               row.append(0)
        bm.append(row)
    return TEMPLATE_STATIC % (name, pformat(bm))


def import_dir(name, target):
    frames = []
    images = [f for f in os.listdir(target) if f.endswith(".png")]
    for img in images:
        img = Image.open(os.path.join(target ,img))
        pixels = img.load()
        bm = [] # binary matrix
        for i in range(0, img.height):
            row = []
            for j in range(0, img.width):
                if pixels[j,i] == (0,0,0,255):
                   row.append(1)
                else:
                   row.append(0)
            bm.append(row)
        frames.append(bm)
    return TEMPLATE_ANIM % (name, len(frames) -1, pformat(frames))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('./importer.py <name> <target> <el_type>')
        sys.exit(1)

    name = sys.argv[1]
    target = sys.argv[2]
    el_type = sys.argv[3]

    if el_type == "anim" and os.path.isdir(target):
        print(import_dir(name, target))

    elif el_type == "static" and os.path.isfile(target) :
        print(import_image(name, target))

