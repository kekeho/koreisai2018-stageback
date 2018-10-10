from flask import Flask, render_template, request, redirect, url_for
import os
from lib import LEDObject

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['全体点滅',
                '交互に点滅',
                '全体レインボー', 'レインボー進行',
                '光の進行',
                'P', 'a', 'i', 'n', 't', 'e', 'r']

speed_list = ['1x', '2x', '4x', '8x', '16x']

led = LEDObject()


@app.route('/')
def index():
    return render_template('index.html', now_pattern=led.now_pattern, pattern_list=pattern_list, 
                            pattern_length_div_by_3_int=int(len(pattern_list) / 3),
                            speed_list=speed_list, speed_length_div_by_3_int=int(len(speed_list) / 3),
                            now_speed=led.now_speed)


@app.route('/set', methods=['POST'])
def set_pattern():
    global now_pattern
    global led

    if led.running_pipe:
        led.running_pipe.kill()
        led.running_pipe = None

    print(request.form.getlist('pattern'))

    request_pattern_list = request.form.getlist('pattern')
    request_speed_list = request.form.getlist('speed')
    request_pattern = None
    request_speed = None

    if len(request_pattern_list) != 0:
        request_pattern = request_pattern_list[0]
    elif len(request_speed_list) != 0:
        request_speed = request_speed_list[0]
    else:
        raise ValueError

    if request_pattern:
        if request_pattern == 'clear':
            # LEDすべてOFF
            led.off()
        elif request_pattern == 'allwhite':
            led.on()
            led.show()
        else:
            led.animation(request_pattern)

        led.now_pattern = request_pattern

    elif request_speed:
        print('SPEED:', request_speed) #debug
        led.animation(led.now_pattern, option1=request_speed)
        led.now_speed = request_speed
    else:
        raise ValueError()
        

    print('GET:', request_pattern, request_speed)  # debug
    # TODO: 余裕があれば、実際にRaspberry Pi側から完了信号が届いてからnow_patternを更新
  
    return redirect('/')


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
