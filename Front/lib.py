import sys
import os
import time
import argparse
import subprocess
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIRNAME + '/../lib/python')
from neopixel import *

# LED strip configuration:
LED_COUNT = 1093      # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
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

    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
            LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.num_pixels = self.strip.numPixels()
        self.now_status = 'off'  # ON or OFF
        self.now_pattern = ' '  # animation pattern
        self.now_color = ['000000' for i in range(self.num_pixels)]  # color list
        self.now_speed = '1x'

        self.painter = {'P': range(0, 203), 'a': range(203, 396),
                        'i': range(396, 510), 'n': range(510, 677),
                        't': range(677, 795), 'e': range(795, 986),
                        'r': range(986, 1093)}

        self.round_painter = {'P': round('P'), 'a': round('a')

        }

        self.running_pipe = None
        self.strip.begin()

    def on(self):
        """turn all LED ON (WHITE/0xffffff)"""
        self.color('ffffff')
        self.now_status = 'on'

    def off(self):
        """"turn all LED OFF"""
        self.color('000000')
        self.show()
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

    def show(self):
        self.strip.show()
        self.now_status = 'on'

    def pixel_shift(self):
        self.now_color.insert(0, self.now_color.pop())
        for i, hexcolor in enumerate(self.now_color):
            self.color(hexcolor, i)

    def animation(self, pattern: str, option1=None, option2=None):
        """set animation
        option1=Speed
        option2=Color
        """
        print('in the animation')  # debug
        print(pattern, option1, option2)
        if option1 and option2:
            self.running_pipe = subprocess.Popen(
                ['python3', CURRENT_DIRNAME + '/animation.py', pattern, 'option1=' + option1, 'option2=' + option2])
        elif option1:
            self.running_pipe = subprocess.Popen(
                ['python3', CURRENT_DIRNAME + '/animation.py', pattern, 'option1=' + option1])
        elif option2:
            self.running_pipe = subprocess.Popen(
                ['python3', CURRENT_DIRNAME + '/animation.py', pattern, 'option2=' + option2])
        else:
            self.running_pipe = subprocess.Popen(
                ['python3', CURRENT_DIRNAME + '/animation.py', pattern])

        self.now_status = 'on'


def round(char: str):
    if len(char) != 1:
        raise ValueError
    
    if char == 'P':
        P = [list(range(145, 148)) + list(range(0, 4))]
        for i, j in zip(range(125, 145)[::-1], range(4, 24)):
            P.append([i, j])
        for i in range(116, 125)[::-1]:
            P.append([i])
        for i, j in zip(range(99, 116)[::-1], list(range(193, 203))+list(range(148, 155))):
            P.append([i, j])
        for i in range(86, 99)[::-1]:
            P.append([i])

        previous_j = None
        for i in range(24, 86)[::-1]:
            j = int(155 + (193-155) / (86-24) * (-1*i + 86))
            if previous_j == j:
                P.append([i])
            else:
                previous_j = j
                P.append([i, j])
        return P

        

def main():
    led = LEDObject()
    led.off()
    led.animation('blink', option2='00ff00')


if __name__ == '__main__':
    main()
