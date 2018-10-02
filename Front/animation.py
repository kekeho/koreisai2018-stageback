import sys
import time
from lib import LEDObject

# python3 animation.py pattern option1=xxx option2=xxx


def animation_blink(led: LEDObject, sleepsec=0.5, hexcolor='ffffff'):
    # init
    led.off()
    while True:
        led.color(hexcolor)
        time.sleep(sleepsec)

        led.off()
        time.sleep(sleepsec)


def animation_alternating_flashing(led: LEDObject, sleepsec=0.5, hexcolor='ffffff', dist=3):
    # init
    while True:
        led.off()
        for i in range(0, led.strip.numPixels(), dist*2):
            for j in range(0, dist):
                if i+j >= led.strip.numPixels():
                    break;
                led.color(hexcolor, position=i+j)
            for j in range(dist, dist*2):
                if i+j >= led.strip.numPixels():
                    break;
                led.color('000000', position=i+j)
        time.sleep(sleepsec)

        led.off()
        for i in range(0, led.strip.numPixels(), dist*2):
            for j in range(0, dist):
                if i+j >= led.strip.numPixels():
                    break;
                led.color('000000', position=i+j)
            for j in range(dist, dist*2):
                if i+j >= led.strip.numPixels():
                    break;
                led.color(hexcolor, position=i+j)
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
    animation_blink(led, sleepsec=0.5/2)

if pattern == '全体点滅 4x':
    animation_blink(led, sleepsec=0.5/4)

if pattern == '全体点滅 8x':
    animation_blink(led, sleepsec=0.5/8)

if pattern == '交互に点滅':
    animation_alternating_flashing(led, dist=4)