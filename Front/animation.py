import sys
import time
import colorsys
from lib import LEDObject


painter = {'P': range(0, 194), 'a': range(194, 390),
           'i': range(390, 507), 'n': range(507, 677),
           't': range(677, 795), 'e': range(795, 986),
           'r': range(986, 1093)}

# python3 animation.py pattern option1=xxx option2=xxx


def animation_blink(led: LEDObject, speed: int, hexcolor: str):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'

    print(speed, hexcolor)  # debug

    sleepsec = 0.2
    # init
    led.off()
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
        led.off()
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

        led.off()
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
    led.off()  # init
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
    led.off()  # init
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
            led.off()  # clear
            for j in range(block):
                led.color(hexcolor, position=i + j)
            led.show()
            time.sleep(sleepsec / speed)


def string(led: LEDObject, hexcolor: str, char: str):
    """
    lightup only single char
    warning: this method does not clear other pixel
    """
    if len(char) != 1:
        raise ValueError

    if hexcolor == None:
        hexcolor = 'ffffff'

    for i in painter[char]:
        led.color(hexcolor, position=i)
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


if pattern == '全体点滅':
    # 全体点滅アニメーション
    animation_blink(led, speed=option1, hexcolor=option2)

if pattern == '交互に点滅':
    animation_alternating_flashing(led, speed=option1, hexcolor=option2)

if pattern == '全体レインボー':
    animation_rainbow(led)

if pattern == 'レインボー進行':
    animation_rainbow_flow(led, speed=option1)

if pattern == '光の進行':
    animation_flow(led, speed=option1, hexcolor=option2)


if pattern == 'P':
    led.off()
    string(led, hexcolor=option2, char='P')

if pattern == 'a':
    led.off()
    string(led, hexcolor=option2, char='a')

if pattern == 'i':
    led.off()
    string(led, hexcolor=option2, char='i')

if pattern == 'n':
    led.off()
    string(led, hexcolor=option2, char='n')

if pattern == 't':
    led.off()
    string(led, hexcolor=option2, char='t')

if pattern == 'e':
    led.off()
    string(led, hexcolor=option2, char='e')

if pattern == 'r':
    led.off()
    string(led, hexcolor=option2, char='r')
