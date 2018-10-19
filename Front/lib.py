import sys
import os
import time
import argparse
import colorsys
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
# set include path to openPurikura directory
sys.path.append(CURRENT_DIRNAME + '/../lib/python')
from neopixel import *

# LED strip configuration:
LED_COUNT = 1092      # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
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
        self.show()
        self.now_status = 'off'


    def brightness(self, value: int):
        self.strip.setBrightness(value)
        self.show()


    def color(self, hex_color: str, *position: int):
        """set LED color with hex (RGB)
        default: ALL LEDs color turns hex value
        if you set potition, only a LED in the position turns hex value"""
        color = Color(int(hex_color[2:4], base=16),
                      int(hex_color[:2], base=16),
                      int(hex_color[4:6], base=16))
        if(position):
            # turn to this color only 1 pixel
            self.strip.setPixelColor(position[0], color)
            self.now_color[position[0]] = int_to_hexcolor(color, 'lib')
        else:
            self.now_color = [] #リセット
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
                self.now_color.append(int_to_hexcolor(color, 'lib'))
        
    
    def show(self):
        self.strip.show()
        self.now_status = 'on'


    def on_rainbow(self, circle_width: int):
        # set rainbow
        for i in range(0, self.num_pixels, circle_width):
            for j in range(0, circle_width):
                if i + j >= self.num_pixels:
                    break

                h = 1 / circle_width * j
                r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
                hex_rgb = [hex(int(r * 255)).split('0x')[-1], hex(int(g * 255)
                                                                ).split('0x')[-1], hex(int(b * 255)).split('0x')[-1]]
                hexcolor = ''
                for color in hex_rgb:
                    if len(color) == 1:
                        color = '0' + color
                    hexcolor += color
                self.color(hexcolor, i + j)
        self.show()


    def animation(self, pattern: str):
        """set animation
        """
        pass
        # if pattern is 'blink':
        #     led.off

        # self.now_status = 'on'


def main():
    led = LEDObject()
    led.off()
    time.sleep(1)
    led.on()
    led.color('ff0000', 3)


if __name__ == '__main__':
    main()
