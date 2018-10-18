from flask import Flask, render_template, request, redirect, url_for
import os
from lib import LEDObject
from matplotlib import colors

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['blink', 'hoge', 'fuga', 'nyan', 'kiee']
color_list = ['white', 'red', 'green', 'blue', 'yellow', 'hotpink', 'aqua', 'darkorange', 'lime']

now_color_button = 'white'
now_pattern = ' '
led = LEDObject()


@app.route('/')
def index():
    return render_template('index.html', now_pattern=now_pattern, pattern_list=pattern_list, 
                            pattern_length_div_by_3_int=int(len(pattern_list) / 3),
                            color_list=color_list, color_length_div_by_3_int=int(len(color_list)/3))


@app.route('/set', methods=['POST'])
def set_pattern():
    global now_pattern
    global now_color_button
    global led
    request_pattern = request.form.getlist('pattern')
    request_color = request.form.getlist('color')
    print('REQ COL:', request_color)

    if request_pattern:
        if request_pattern[0] == 'clear':
            # LEDすべてOFF
            led.off()
        elif request_pattern[0] == 'MONOCOLOR':
            now_pattern = request_pattern[0]
            hexcolor = colors.cnames[now_color_button][1:].lower()
            led.color(hexcolor)
            print('SET PTN')

    elif request_color:
        now_color_button = request_color[0]
        hexcolor = colors.cnames[now_color_button][1:].lower()
        led.color(hexcolor)
        print('SET COL')

    # TODO: 余裕があれば、実際にRaspberry Pi側から完了信号が届いてからnow_patternを更新
    return redirect('/')


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
