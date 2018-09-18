from flask import Flask, render_template, request, redirect, url_for
import os

CURRENT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder='./templates/assets')
pattern_list = ['blink', 'hoge', 'fuga', 'nyan', 'kiee']

@app.route('/')
def index():
    now_pattern = 'TEST_NOW_PATTERN'
    return render_template('index.html', now_pattern=now_pattern, pattern_list=pattern_list, pattern_length_div_by_3_int=int(len(pattern_list)/3))


@app.route('/set', methods=['POST'])
def set_pattern():
    # TODO: 処理を書く
    # debug
    print('GET:', request.form)
    return redirect('/')

def main():
    app.debug = True
    app.run()

if __name__ == '__main__':
    main()