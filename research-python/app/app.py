import json
import traceback
#import fasttext as ft
from flask import Flask, request, render_template
import re
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
sys.path.append(dir_path+"/../modules/")
from data_crawler.data_prep import CodePreprocess
import api_twitter

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        return render_template('index.html')
    else:

        textMin = 1
        textMax = 20
        isPost = 1

        error = "見つけなかった。"
        language = ""
        code = ""

        try:
            code = request.form['code']

            if not code or len(code) < textMin or len(code) > textMax:
                error = 'Please 「投稿リスト」 from '+format(textMin)+' to '+format(textMax)+' characters!'
            else:
                #language, score = ci.pred(code)
                language = api_twitter.main(code)
                error = "見つけなかった。"

        except:
            #traceback.print_exc()
            error = traceback.format_exc() + 'Unknown error has occurred, please try again!'
            
        return render_template('index.html', language=language, ispost=isPost, code=code, error=error)

if __name__ == '__main__':
    app.run(debug=True)
