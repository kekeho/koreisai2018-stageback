import sys
import os
import time
import argparse
CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))
# set include path to openPurikura directory
sys.path.append(CURRENT_DIRNAME + '/../lib/python')
from neopixel import *

# LED strip configuration:
LED_COUNT = 32      # Number of LED pixels.
LED_PIN = 12      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class LEDObject():
    """Koreisai StageBack LED-Logo Object
    """
    now_status = 'off'  # ON or OFF
    now_pattern = None  # animation pattern

    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
            LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def on(self):
        """turn all LED ON"""
        pass

    def off(self):
        """"turn all LED OFF"""
        pass

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
        else:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, color)
        self.strip.show()
       

    def animation(self, pattern: str):
        """set animation
        Return:
            1 or -1 (Success or Failure)
        """
        pass


def main():
    led = LEDObject()
    led.color('ffffff')
    led.color('ff0000', 3)


if __name__ == '__main__':
    main()
