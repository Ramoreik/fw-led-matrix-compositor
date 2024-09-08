#!/usr/bin/env python3
import random
import threading
from compositor import Element, Compositor, Static


class Snowflake(Static):
    def __init__(self):
        self.center = [0,0]
        self.frame = [
                        [1],
                      ]


def snowfall(device):

    def add():
        xpos = 0
        ypos = 0
        if xpos == 0:
            ypos = random.randint(0, 34)
        position = [xpos, ypos ]
        fall_speed = random.randint(-2, -1)
        wind = 0 # wind
        if random.randint(0, 100) <= 100:
            wind = -1 # wind
        vector = [wind, fall_speed ]
        c.add_element(Element(Snowflake(), vector, position))

    c = Compositor([9, 34], device)
    while True:
        add()
        if random.randint(0, 100) <= 70:
            add()
        c.render()


def both_device_snowfall():
    DEVICE1 = "/dev/ttyACM0"
    DEVICE2 = "/dev/ttyACM1"
    dev1 = threading.Thread(target=snowfall, args=(DEVICE1,))
    dev2 = threading.Thread(target=snowfall, args=(DEVICE2,))
    dev1.start()
    dev2.start()
    dev1.join()
    dev2.join()


if __name__ == "__main__":
    both_device_snowfall()
