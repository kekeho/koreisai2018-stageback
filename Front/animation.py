import sys
import time
from lib import LEDObject

# python3 animation.py pattern option1=xxx option2=xxx


def animation_blink(led: LEDObject, sleepsec=0.2, hexcolor='ffffff'):
    # init
    led.off()
    while True:
        led.color(hexcolor)
        time.sleep(sleepsec)

        led.off()
        time.sleep(sleepsec)


def animation_alternating_flashing(led: LEDObject, sleepsec=0.2, hexcolor='ffffff', dist=3):
    # init
    while True:
        led.off()
        for i in range(0, led.strip.numPixels(), dist * 2):
            for j in range(0, dist):
                if i + j >= led.strip.numPixels():
                    break
                led.color(hexcolor, position=i + j)
            for j in range(dist, dist * 2):
                if i + j >= led.strip.numPixels():
                    break
                led.color('000000', position=i + j)
        time.sleep(sleepsec)

        led.off()
        for i in range(0, led.strip.numPixels(), dist * 2):
            for j in range(0, dist):
                if i + j >= led.strip.numPixels():
                    break
                led.color('000000', position=i + j)
            for j in range(dist, dist * 2):
                if i + j >= led.strip.numPixels():
                    break
                led.color(hexcolor, position=i + j)
        time.sleep(sleepsec)


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


def animation_rainbow(led: LEDObject, sleepsec=0.02, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    while True:
        for j in range(256 * iterations):
            for i in range(led.strip.numPixels()):
                led.color(wheel((i + j) & 255), position=i)
            time.sleep(sleepsec)


def animation_rainbow_cycle(led: LEDObject, sleepsec=0.02, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    while True:
        for j in range(256*iterations):
            for i in range(led.strip.numPixels()):
                led.color(wheel((int(i * 256 / led.strip.numPixels()) + j) & 255), position=i)
            time.sleep(sleepsec)


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
            option1 = sys.argv[i][8:]
        if 'option2=' in sys.argv[i]:
            option2 = sys.argv[i][8:]


if pattern == '全体点滅':
    # 全体点滅アニメーション
    animation_blink(led)

if pattern == '全体点滅 2x':
    animation_blink(led, sleepsec=0.2 / 2)

if pattern == '全体点滅 4x':
    animation_blink(led, sleepsec=0.2 / 4)

if pattern == '全体点滅 8x':
    animation_blink(led, sleepsec=0.2 / 8)

if pattern == '交互に点滅':
    animation_alternating_flashing(led, dist=4)

if pattern == '交互に点滅 2x':
    animation_alternating_flashing(led, sleepsec=0.2/2, dist=4)

if pattern == '交互に点滅 4x':
    animation_alternating_flashing(led, sleepsec=0.2/4, dist=4)

if pattern == '交互に点滅 8x':
    animation_alternating_flashing(led, sleepsec=0.2/8, dist=4)

if pattern == '全体レインボー':
    animation_rainbow(led)

if pattern == 'レインボー進行':
    animation_rainbow_cycle(led)
