import sys
import time
from lib import LEDObject

# python3 animation.py pattern option1=xxx option2=xxx


def animation_blink(led: LEDObject, sleepsec=0.5, hexcolor='ffffff'):
    while True:
        led.off()
        time.sleep(sleepsec)
        led.color(led.now_color)
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


if pattern == 'blink':
    # 点滅アニメーション
    if option1 and option2:
        animation_blink(led, sleepsec=float(option1), hexcolor=option2)
    elif option1:
        animation_blink(led, sleepsec=float(option1))
    elif option2:
        animation_blink(led, hexcolor=option2)
    else:
        animation_blink(led)
