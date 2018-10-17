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


def animation_alternating_flashing(led: LEDObject, speed: int, hexcolor: str, dist=3):
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


def animation_rainbow(led: LEDObject, circle_width=50):
    # set rainbow
    for i in range(0, led.num_pixels, circle_width):
        for j in range(0, circle_width):
            if i + j >= led.num_pixels:
                break

            h = 1 / circle_width * j
            print('h', h)
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            hex_rgb = [hex(int(r * 255)).split('0x')[-1], hex(int(g * 255)
                                                              ).split('0x')[-1], hex(int(b * 255)).split('0x')[-1]]
            hexcolor = ''
            for color in hex_rgb:
                if len(color) == 1:
                    color = '0' + color
                hexcolor += color

            print(hexcolor)
            led.color(hexcolor, i + j)
    led.show()


def animation_rainbow_flow(led: LEDObject, speed: int, circle_width=50):
    if speed == None:
        speed = 1

    """Draw rainbow that uniformly distributes itself across all pixels."""
    sleepsec = 0.1
    # set rainbow
    for i in range(0, led.num_pixels, circle_width):
        for j in range(0, circle_width):
            if i + j >= led.num_pixels:
                break

            h = 1 / circle_width * j
            print('h', h)
            r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
            hex_rgb = [hex(int(r * 255)).split('0x')[-1], hex(int(g * 255)
                                                              ).split('0x')[-1], hex(int(b * 255)).split('0x')[-1]]
            hexcolor = ''
            for color in hex_rgb:
                if len(color) == 1:
                    color = '0' + color
                hexcolor += color

            print(hexcolor)
            led.color(hexcolor, i + j)
    while True:
        led.show()
        time.sleep(sleepsec / speed**2)
        led.pixel_shift()


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

# init
led.off()

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

if pattern == 'Advance':
    animation_flow(led, speed=option1, hexcolor=option2)

if pattern == 'Pain':
    pain(led, hexcolor=option2)


if pattern == 'P':
    animation_round(led, 'P', speed=option1, hexcolor=option2)

if pattern == 'a':
    animation_round(led, 'a', speed=option1, hexcolor=option2)

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
