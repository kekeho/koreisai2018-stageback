from flask import Flask, render_template, request, redirect, url_for
import os

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['blink', 'hoge', 'fuga', 'nyan', 'kiee']

now_pattern = ' '

@app.route('/')
def index():
    return render_template('index.html', now_pattern=now_pattern, pattern_list=pattern_list, pattern_length_div_by_3_int=int(len(pattern_list)/3))


@app.route('/set', methods=['POST'])
def set_pattern():
    global now_pattern
    # TODO: 処理を書く
    # debug
    print('GET:', request.form['pattern'])
    # TODO: 余裕があれば、実際にRaspberry Pi側から完了信号が届いてからnow_patternを更新
    now_pattern = request.form['pattern']
    return redirect('/')

def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()