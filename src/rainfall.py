#!/usr/bin/env python3
import random
import threading
from compositor import Element, Compositor, Anim


class Rainfall(Anim):
    def __init__(self):
        self.tick = 0
        self.reset = 4
        self.tick_rate = 1
        self.center = [0,0]
        self.frames = [
                          [
                            [1,0,0],
                            [0,1,0],
                            [0,0,0]
                          ],
                          [
                            [1,0,0],
                            [0,1,0],
                            [0,0,1]
                          ],
                          [
                            [1,0,0,0],
                            [0,1,0,0],
                            [0,0,1,0],
                            [0,0,0,1],
                          ],
                          [
                            [1,0,0,0],
                            [0,1,0,0],
                            [0,0,1,0],
                            [0,0,0,1],
                          ],
                          [
                            [1,0,0,0,0],
                            [0,1,0,0,0],
                            [0,0,1,0,0],
                            [0,0,0,1,0],
                            [0,0,0,0,1],
                          ],
                          [
                            [1,0,0,0,0,0],
                            [0,1,0,0,0,0],
                            [0,0,1,0,0,0],
                            [0,0,0,1,0,0],
                            [0,0,0,0,1,0],
                            [0,0,0,0,0,1],
                          ],

                       ]


def rainfall(device):
    def add():
        xpos = 0
        ypos = 0
        if xpos == 0:
            ypos = random.randint(0, 30)
        position = [xpos, ypos ]
        fall_speed = random.randint(-2, -1)
        wind = 0 # wind
        if random.randint(0, 100) <= 50:
            wind = -1 # wind
        vector = [-1 + wind, fall_speed ]
        c.add_element(Element(Rainfall(), vector, position))

    c = Compositor([9, 34], device)

    while True:
        add()
        add()
        c.render()
        #time.sleep(0.05)


def both_device_rainfall():
    DEVICE1 = "/dev/ttyACM0"
    DEVICE2 = "/dev/ttyACM1"
    dev1 = threading.Thread(target=rainfall, args=(DEVICE1,))
    dev2 = threading.Thread(target=rainfall, args=(DEVICE2,))
    dev1.start()
    dev2.start()
    dev1.join()
    dev2.join()

if __name__ == "__main__":
    both_device_rainfall()

