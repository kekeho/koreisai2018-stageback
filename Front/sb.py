from flask import Flask, render_template, request, redirect, url_for
import os
from lib import LEDObject
from matplotlib import colors
import subprocess

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['Blink',
                'Alternately Blink',
                'Rainbow', 'Rainbow Animation', 'Rainbow Long',
                'Advance',
                'Pain',
                'P', 'a', 'i', 'n', 't', 'e', 'r']

speed_list = ['1x', '2x', '4x', '8x', '16x']

color_list = ['white', 'red', 'green', 'blue', 'yellow', 'hotpink', 'aqua', 'darkorange', 'lime', 'rainbow']

now_color_button = 'white'
now_pattern = ' '
now_brightness = 255
led = LEDObject()


@app.route('/')
def index():
    return render_template('index.html', now_pattern=now_pattern, now_brightness=str(now_brightness), now_color=now_color_button, pattern_list=pattern_list, 
                            pattern_length_div_by_3_int=int(len(pattern_list) / 3),
                            color_list=color_list, color_length_div_by_3_int=int(len(color_list)/3))


@app.route('/set', methods=['POST'])
def set_pattern():
    global now_pattern
    global now_color_button
    global led
    global now_brightness

    if led.running_pipe:
        led.running_pipe.kill()
        print('KILL PROCESS') #debug
        led.running_pipe = None

    
    print(request.form.getlist('pattern'))

    request_pattern_list = request.form.getlist('pattern')
    request_speed_list = request.form.getlist('speed')
    request_color_list = request.form.getlist('color')
    request_pattern = None
    request_speed = None
    request_color = None

    if len(request_pattern_list) != 0:
        request_pattern = request_pattern_list[0]
    elif len(request_speed_list) != 0:
        request_speed = request_speed_list[0]
    elif len(request_color_list) != 0:
        request_color = request_color_list[0]
    else:
        raise ValueError

    if request_pattern:
        if request_pattern[0] == 'clear':
            # LEDすべてOFF
            led.off()
        else:
            if led.now_color_button == 'rainbow':
                led.animation(request_pattern, option1=led.now_speed, option2=led.now_color_button)
            else:
                hexcolor = colors.cnames[now_color_button][1:].lower()
                led.color(hexcolor)
                print('SET PTN')
            led.show()

    elif request_color:
        now_color_button = request_color[0]
        if request_color[0] == 'rainbow':
            led.on_rainbow(70)

        elif request_color[0] == 'default':
            led.default_color()
        else:
            hexcolor = colors.cnames[now_color_button][1:].lower()
            led.color(hexcolor)
            led.show()

    # TODO: 余裕があれば、実際にRaspberry Pi側から完了信号が届いてからnow_patternを更新
    if led.running_pipe:
        runnning_pid = led.running_pipe.pid
        with open(CURRENT_DIRNAME + '/pid.log', mode='w') as logfile:
            logfile.write(str(runnning_pid))

    return redirect('/')


def main():
    with open(CURRENT_DIRNAME + '/pid.log', 'r') as pid_log:
        running_pid = pid_log.read()
        if running_pid:
            print('KILL PROCESS') # debug
            subprocess.run(['sudo', 'kill', running_pid])

    app.debug = True
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        led.off()
        if led.running_pipe:
            led.running_pipe.kill()

