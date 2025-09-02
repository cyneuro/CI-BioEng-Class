frequency = 3.917727717925015

from microbit import *

def update_screen(frequency):
    _wait_time = 1000 / (2 * frequency)
    display.set_pixel(2, 2, 9)
    sleep(_wait_time)
    display.set_pixel(2, 2, 0)
    sleep(_wait_time)

while True:
    update_screen(frequency)