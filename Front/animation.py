import sys
import time
import colorsys
from lib import LEDObject


# python3 animation.py pattern option1=xxx option2=xxx


def default(led: LEDObject):
    painter_color = ['ff8200', '5555ff', '1fff00',
                     'fff400', 'ff00d2', '0029ff', 'ff1010']
    for hexcolor, char in zip(painter_color, 'Painter'):
        string(led, hexcolor, char)
    led.show()


def animation_blink(led: LEDObject, speed: int, hexcolor: str):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'
    sleepsec = 0.2

    if hexcolor == 'rainbow':
        animation_rainbow(led)
        color_list = led.get_now_color()
        while True:
            for i, color in enumerate(color_list):
                led.color(color, position=i)
            led.show()
            time.sleep(sleepsec / speed)
            led.off()
            time.sleep(sleepsec / speed)
    else:
        while True:
            led.color(hexcolor)
            led.show()
            time.sleep(sleepsec / speed)

            led.off()
            time.sleep(sleepsec / speed)


def animation_alternating_flashing(led: LEDObject, speed: int, hexcolor: str, dist=6):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'

    sleepsec = 0.2
    while True:
        led.color('000000')
        for i in range(0, led.num_pixels, dist * 2):

            for j in range(0, dist):
                if i + j >= led.num_pixels:
                    break
                led.color(hexcolor, position=i + j)
            for j in range(dist, dist * 2):
                if i + j >= led.num_pixels:
                    break
                led.color('000000', position=i + j)
        led.show()
        time.sleep(sleepsec / speed)

        led.color('000000')
        for i in range(0, led.num_pixels, dist * 2):
            for j in range(0, dist):
                if i + j >= led.num_pixels:
                    break
                led.color('000000', position=i + j)
            for j in range(dist, dist * 2):
                if i + j >= led.num_pixels:
                    break
                led.color(hexcolor, position=i + j)
        led.show()
        time.sleep(sleepsec / speed)


def animation_rainbow(led: LEDObject, circle_width=60):
    # set rainbow
    for i in range(0, led.num_pixels, circle_width):
        for j in range(0, circle_width):
            if i + j >= led.num_pixels:
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

            led.color(hexcolor, i + j)
    led.show()


def static(led: LEDObject, hexcolor):
    led.color(hexcolor)
    led.show()


def animation_rainbow_flow(led: LEDObject, speed: int, circle_width=60):
    if speed == None:
        speed = 1

    """Draw rainbow that uniformly distributes itself across all pixels."""
    # set rainbow
    for i in range(0, led.num_pixels, circle_width):
        for j in range(0, circle_width):
            if i + j >= led.num_pixels:
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

            led.color(hexcolor, i + j)
    while True:
        led.show()
        led.pixel_shift(pixel_num=speed)


def animation_flow(led: LEDObject, speed: int, hexcolor: str, block=2):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'

    sleepsec = 0.1
    while True:
        for i in range(0, led.num_pixels, block):
            led.color('000000')  # clear
            for j in range(block):
                led.color(hexcolor, position=i + j)
            led.show()
            time.sleep(sleepsec / speed)


def string(led: LEDObject, hexcolor: str, char: str):
    """
    set color only single char
    warning: this method does not clear other pixel
    """
    if len(char) != 1:
        raise ValueError

    if hexcolor == None:
        hexcolor = 'ffffff'

    for i in led.painter[char]:
        led.color(hexcolor, position=i)


def pain(led: LEDObject, hexcolor: str):
    if hexcolor == None:
        hexcolor = 'ff0000'

    if hexcolor == 'rainbow':
        animation_rainbow(led)
        for char in 'ter':
            string(led, '000000', char)
        led.show()

    else:
        for char in 'Pain':
            string(led, hexcolor, char)
        for char in 'ter':
            string(led, '000000', char)
        led.show()


def animation_round(led: LEDObject, char: str,speed: int, hexcolor: str):
    if len(char) != 1:
        raise ValueError
    
    # Init
    led.off()
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'

    for count, line in enumerate(led.round_painter[char]):
        for pixel in line:
            led.color(hexcolor, pixel)
        if count%speed == 0: 
            led.show()
            time.sleep(0.001/speed)
    led.show()


def rainbow_long(led: LEDObject, iterations=10, speed=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(led.num_pixels):
            led.strip.setPixelColor(i, wheel((int(i * 256 / led.num_pixels) + j) & 255))
        led.show()
        time.sleep(0.0001 / speed**2)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def Color(red, green, blue, white = 0):
	"""Convert the provided red, green, blue color to a 24-bit color value.
	Each color component should be a value 0-255 where 0 is the lowest intensity
	and 255 is the highest intensity.
	"""
	return (white << 24) | (red << 16)| (green << 8) | blue


led = LEDObject()
argc = len(sys.argv)

if argc == 1:
    print('Error: 引数が足りません')
    exit(-1)

pattern = sys.argv[1]
option1 = None
option2 = None

if argc >= 3:
    # オプションが存在
    for i in range(2, argc):
        if 'option1=' in sys.argv[i]:
            option1 = int(sys.argv[i][8:][:-1])
        if 'option2=' in sys.argv[i]:
            option2 = sys.argv[i][8:]


print('ANIMATION:', pattern, option1, option2)

try:
    if pattern == 'static':
        static(led, hexcolor=option2)

    if pattern == 'Default':
        default(led)

    if pattern == 'Blink':
        # 全体点滅アニメーション
        animation_blink(led, speed=option1, hexcolor=option2)

    if pattern == 'Alternately Blink':
        animation_alternating_flashing(led, speed=option1, hexcolor=option2)

    if pattern == 'Rainbow':
        animation_rainbow(led)

    if pattern == 'Rainbow Animation':
        animation_rainbow_flow(led, speed=option1)

    if pattern == 'Rainbow Long':
        rainbow_long(led, speed=option1)

    if pattern == 'Advance':
        animation_flow(led, speed=option1, hexcolor=option2)

    if pattern == 'Pain':
        pain(led, hexcolor=option2)


    if pattern == 'P':
        led.off()
        string(led, hexcolor=option2, char='P')
        led.show()

    if pattern == 'a':
        led.off()
        string(led, hexcolor=option2, char='a')
        led.show()

    if pattern == 'i':
        led.off()
        string(led, hexcolor=option2, char='i')
        led.show()

    if pattern == 'n':
        led.off()
        string(led, hexcolor=option2, char='n')
        led.show()

    if pattern == 't':
        led.off()
        string(led, hexcolor=option2, char='t')
        led.show()

    if pattern == 'e':
        led.off()
        string(led, hexcolor=option2, char='e')
        led.show()

    if pattern == 'r':
        led.off()
        string(led, hexcolor=option2, char='r')
        led.show()

except Exception as e:
    print(e)
    led.off()