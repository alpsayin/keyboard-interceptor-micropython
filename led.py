import time
from machine import Pin, PWM
from micropython import const
from machine import Timer

# LED STATUS INDICATORS
YELLOW = const(0xFF7F07)  # YELLOW
GREEN = const(0x00FF00)  # GREEN
RED = const(0xFF0000)  # RED
BLUE = const(0x0000FF)  # BLUE
PURPLE = const(0xFF0FF0)  # PURPLE
ORANGE = const(0x770F00)  # I WANTED ORANGE, IT GAVE ME LEMON-LIME
WHITE = const(0xFFFFFF)  # WHITE
OFF = const(0x000000)  # HAVE A GUESS

_red_pin = Pin(0)
_green_pin = Pin(2)
_blue_pin = Pin(4)
_red = PWM(_red_pin)
_green = PWM(_green_pin)
_blue = PWM(_blue_pin)
heartbeat_timer = None
heartbeat_color = ORANGE


def rgbled(value=None):
    if value is None:
        return _red.duty()<<16 | _green.duty()<<8 | _blue.duty()
    else:
        _red.duty((value >> 16) & 0xFF)
        _green.duty((value >> 8) & 0xFF)
        _blue.duty(value & 0xFF)


def rainbow():
    # '0ToGreen' : 0 1 0
    # 'GreenToRed': 1 -1 0
    # 'RedToBlue': -1 0 1
    rainbow_pattern = [[0,1,0],[1,-1,0],[-1,0,1],[0,0,-1]]
    colour_cycle(rainbow_pattern)


def colour_cycle(pattern):
    for i in pattern:
        for j in colour_change(i):
            rgbled(j)


def colour_change(flags, colourRange=256):
    for i in range(colourRange):
        yield int('%02x%02x%02x' % tuple([z*i%colourRange for z in flags]), 16)


def heartbeat_cb(timer_obj):
    global heartbeat_timer, heartbeat_color
    # ledval = rgbled()
    # print(timer_obj)
    # print('\nrgb:0x{rgb:06x}'.format(rgb=heartbeat_color))
    rgbled(heartbeat_color)
    time.sleep(0.1)
    rgbled(OFF)
    time.sleep(0.1)
    rgbled(heartbeat_color)
    time.sleep(0.1)
    rgbled(OFF)


def heartbeat(active):
    global heartbeat_timer, heartbeat_color
    if not heartbeat_timer:
        heartbeat_timer = Timer(0)
    if active:
        heartbeat_timer.init(
            period=round(1000 / 50.0 * 50),
            mode=Timer.PERIODIC,
            callback=heartbeat_cb
        )
    else:
        heartbeat_timer.deinit()
        heartbeat_timer = None


def init():
    for pwm in [_red, _green, _blue]:
        pwm.freq(255)
    rainbow()
    rgbled(OFF)
