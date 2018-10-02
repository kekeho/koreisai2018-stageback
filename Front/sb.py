from flask import Flask, render_template, request, redirect, url_for
import os
from lib import LEDObject

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['全体点滅', '全体点滅 2x', '全体点滅 4x', '全体点滅 8x',
                '交互に点滅', '交互に点滅 2x', '交互に点滅 4x', '交互に点滅 8x',
                '全体レインボー', 'レインボー進行',
                '光の進行']

now_pattern = ' '
led = LEDObject()


@app.route('/')
def index():
    return render_template('index.html', now_pattern=now_pattern, pattern_list=pattern_list, pattern_length_div_by_3_int=int(len(pattern_list) / 3))


@app.route('/set', methods=['POST'])
def set_pattern():
    global now_pattern
    global led

    if led.running_pipe:
        led.running_pipe.kill()
        led.running_pipe = None

    request_pattern = request.form['pattern']
    if request_pattern == 'clear':
        # LEDすべてOFF
        led.off()
    elif request_pattern == 'allwhite':
        led.on()
    else:
        led.animation(request_pattern)

    print('GET:', request.form['pattern'])  # debug
    # TODO: 余裕があれば、実際にRaspberry Pi側から完了信号が届いてからnow_patternを更新
    now_pattern = request.form['pattern']
    return redirect('/')


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
