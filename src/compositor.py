import time
import random
import tempfile
import threading
from subprocess import check_output

from PIL import Image


DEVICE1 = "/dev/ttyACM0"
DEVICE2 = "/dev/ttyACM1"
CMD = "inputmodule-control --serial-dev '%s' led-matrix --image-bw '%s'"
BRIGHTNESS_CMD = "inputmodule-control --serial-dev '%s' led-matrix --brightness 30"

class Static():
    def __init__(self):
        self.center = [0,0]
        self.frame = []

    def draw(self, position):
        positions = []
        x, y = position
        xc, yc = self.center

        ym = 0
        for r in self.frame:
            xm = 0
            for c in r:
                if c == 1:
                    xr = xm - xc 
                    yr = ym - yc
                    xn = x + xr
                    yn = y + yr
                    positions.append([xn, yn])

                xm = xm + 1
                if xm > len(r):
                    xm = 0

            ym = ym + 1
            if ym > len(self.frame):
                ym = 0

        return positions


class Anim():
    def __init__(self):
        self.tick = 0
        self.tick_rate = 0.5
        self.reset = 0
        self.center = [0,0]
        self.frames = [[]]

    def draw(self, position):

        positions = []
        x, y = position
        xc, yc = self.center

        frame = self.frames[round(self.tick)]
        ym = 0
        for r in frame:
            xm = 0
            for c in r:
                if c == 1:
                    xr = xm - xc 
                    yr = ym - yc
                    xn = x + xr
                    yn = y + yr
                    positions.append([xn, yn])

                xm = xm + 1
                if xm > len(r):
                    xm = 0

            ym = ym + 1
            if ym > len(frame):
                ym = 0

        self.tick = self.tick + ( 1 * self.tick_rate )
        if self.tick > self.reset:
            self.tick = 0
        return positions


class Element:
    def __init__(self, pattern, vector, position):
        self.pattern = pattern
        self.vector = vector
        self.position = position
        self.first_tick = True

    def calculate(self):
        x, y = self.position
        xv, yv = self.vector
        if not self.first_tick:
            self.position = [x - xv, y - yv]
        else:
            self.first_tick = False
        return self.pattern.draw(self.position)


class Compositor:

    WHITE = 1

    def __init__(self, dimensions, device):
        self.elements = []
        self.dimensions = dimensions
        self.device = device
        self.outdir = tempfile.TemporaryDirectory()
        check_output(BRIGHTNESS_CMD % self.device, shell=True)

    def add_element(self, element):
        self.elements.append(element)

    def render(self):
        img = Image.new('1', self.dimensions)
        xd, yd = self.dimensions
        pixels = img.load()

        for element in self.elements:
            oob = 0
            positions = element.calculate()

            for position in positions:
                x, y  = position
                if abs(x) < xd and abs(y) < yd:
                    pixels[x, y] = self.WHITE
                else:
                    # out of bounds counter
                    oob = oob + 1

            # eliminate completely out of bounds object
            if oob == len(positions):
                self.elements.remove(element)

        device_name = self.device.split('/')[2]
        img.save(f"{self.outdir.name}/{device_name}.png", format="png") 
        del img
        del pixels
        check_output(CMD % (self.device, f"{self.outdir.name}/{device_name}.png"), shell=True)
