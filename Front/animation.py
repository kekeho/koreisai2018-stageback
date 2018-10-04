import sys
import time
from lib import LEDObject

# python3 animation.py pattern option1=xxx option2=xxx


def animation_blink(led: LEDObject, speed: int, hexcolor: str):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'

    print(speed, hexcolor) #debug

    sleepsec = 0.2
    # init
    led.off()
    while True:
        led.color(hexcolor)
        time.sleep(sleepsec/speed)

        led.off()
        time.sleep(sleepsec/speed)


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
        time.sleep(sleepsec/speed)

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
        time.sleep(sleepsec/speed)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    # GRB
    if pos < 85:
        return '{:02x}{:02x}{:02x}'.format(255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return '{:02x}{:02x}{:02x}'.format(0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return '{:02x}{:02x}{:02x}'.format(pos * 3, 0, 255 - pos * 3)


def animation_rainbow(led: LEDObject, speed: int, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    if speed == None:
        speed = 1

    sleepsec = 0.02
    led.off() #init
    while True:
        for j in range(256 * iterations):
            for i in range(led.num_pixels):
                led.color(wheel((i + j) & 255), position=i)
            time.sleep(sleepsec/speed)


def animation_rainbow_cycle(led: LEDObject, speed: int, iterations=5):
    if speed == None:
        speed = 1

    """Draw rainbow that uniformly distributes itself across all pixels."""
    sleepsec = 0.02
    led.off() #init
    while True:
        for j in range(256*iterations):
            for i in range(led.num_pixels):
                led.color(wheel((int(i * 256 / led.num_pixels) + j) & 255), position=i)
            time.sleep(sleepsec/speed)


def animation_flow(led: LEDObject, speed: int,hexcolor: str, block=2):
    if speed == None:
        speed = 1
    if hexcolor == None:
        hexcolor = 'ffffff'
    
    sleepsec = 0.1
    while True:
        for i in range(0, led.num_pixels, block):
            led.off() #clear
            for j in range(block):
                led.color(hexcolor, position=i+j)
            time.sleep(sleepsec/speed)



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
    animation_rainbow(led, speed=option1)

if pattern == 'レインボー進行':
    animation_rainbow_cycle(led, speed=option1)

if pattern == '光の進行':
    animation_flow(led, speed=option1, hexcolor=option2)
