import sys
import os
import time
import argparse
import subprocess
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
# set include path to openPurikura directory
sys.path.append(CURRENT_DIRNAME + '/../lib/python')
from neopixel import *

# LED strip configuration:
LED_COUNT = 10      # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 30     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def int_to_hexcolor(num: int, *mode: str):
    """Convert int to hex color
    arg:
        num: int (base=10)
    return:
        hexcolor string like 'ffba78'
    """
    blue = num % 16**2
    num = int(num / 16**2)
    green = num % 16**2
    num = int(num / 16**2)
    red = num % 16**2
    color = {'r': red, 'g': green, 'b': blue}
    if 'lib' in mode:
        # ライブラリのカラーコードだったら(GRB)
        return '{g:02x}{r:02x}{b:02x}'.format(**color)
    else:
        return '{r:02x}{g:02x}{b:02x}'.format(**color)


class LEDObject():
    """Koreisai StageBack LED-Logo Object
    """
    now_status = 'off'  # ON or OFF
    now_pattern = None  # animation pattern
    now_color = []
    string = {'P-inside': range(0, 56)}
    running_pipe = None

    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
            LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.num_pixels = self.strip.numPixels()

    def on(self):
        """turn all LED ON (WHITE/0xffffff)"""
        self.color('ffffff')
        self.now_status = 'on'

    def off(self):
        """"turn all LED OFF"""
        self.color('000000')
        self.now_status = 'on'

    def color(self, hex_color: str, position=None):
        """set LED color with hex (RGB)
        default: ALL LEDs color turns hex value
        if you set potition, only a LED in the position turns hex value"""

        color = Color(int(hex_color[2:4], base=16),
                      int(hex_color[:2], base=16),
                      int(hex_color[4:6], base=16))
        if position != None:
            # turn to this color only 1 pixel
            self.strip.setPixelColor(position, color)
            self.now_color[position] = int_to_hexcolor(color, 'lib')
        else:
            self.now_color = []  # リセット
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
                self.now_color.append(int_to_hexcolor(color, 'lib'))
        self.strip.show()
        self.now_status = 'on'

    def animation(self, pattern: str, option1=None, option2=None):
        """set animation
        """
        print('in the animation')
        if option1 and option2:
            self.running_pipe = subprocess.Popen(['python3', CURRENT_DIRNAME + '/animation.py', pattern,
                                                  'option1={}'.format(option1),
                                                  'option2={}'.format(option2)])
        elif option1:
            self.running_pipe = subprocess.Popen(['python3', CURRENT_DIRNAME + '/animation.py', pattern,
                                                  'option1={}'.format(option1)])
        elif option2:
            self.running_pipe = subprocess.Popen(['python3', CURRENT_DIRNAME + '/animation.py', pattern,
                                                  'option2={}'.format(option2)])
        else:
            self.running_pipe = subprocess.Popen(
                ['python3', CURRENT_DIRNAME + '/animation.py', pattern])

        self.now_status = 'on'


def main():
    led = LEDObject()
    led.off()
    led.animation('blink', option2='00ff00')


if __name__ == '__main__':
    main()
