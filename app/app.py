import json
import traceback
#import fasttext as ft
from flask import Flask, request, render_template
import re
import sys
import os
import xlwt
import time
import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path+"/../")
sys.path.append(dir_path+"/../modules/")
from data_crawler.data_prep import CodePreprocess
import api_twitter

app = Flask(__name__, static_url_path='/asserts', static_folder=dir_path+"/../asserts/")


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
        fileName = ""

        try:
            code = request.form['code']

            if not code or len(code) < textMin or len(code) > textMax:
                error = 'Please 「投稿リスト」 from '+format(textMin)+' to '+format(textMax)+' characters!'
            else:
                #language, score = ci.pred(code)
                language = api_twitter.main(code)
                error = "見つけなかった。"

                style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
                style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
                wb = xlwt.Workbook()
                ws = wb.add_sheet('API')
                ws.write(0, 0, "Search")
                ws.write(0, 1, format(code), style0)

                num = 2
                ws.col(0).width = 0x0d00 + 5000
                ws.col(1).width = 0x0d00 + 20000
                ws.col(2).width = 0x0d00 + 5000

                style2 = xlwt.XFStyle()
                style2.alignment.wrap = 1
                font = xlwt.Font()
                font.bold = True
                style2.font = font
                alignment = xlwt.Alignment()
                alignment.horz = xlwt.Alignment.HORZ_CENTER
                #style2.alignment = alignment

                ws.write(num, 0, "Name", style2)
                ws.write(num, 1, "Text", style2)
                ws.write(num, 2, "Location", style2)

                style = xlwt.XFStyle()
                style.alignment.wrap = 1

                #for item in language:
                i = 0
                while i < len(language):
                    item = language[i]
                    num = num + 1
                    user = item['user']
                    ws.write(num, 0, format(user['name']), style)
                    ws.write(num, 1, format(item['text']), style)
                    ws.write(num, 2, format(user['location']), style)
                    item["created_at2"] = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S %z %Y').timestamp()
                    language[i] = item
                    i = i + 1
                millis = int(round(time.time() * 1000))
                fileName = 'api_file_'+format(millis)+'.xls';

                wb.save(dir_path+"/../asserts/"+fileName)

        except:
            #traceback.print_exc()
            error = traceback.format_exc() + 'Unknown error has occurred, please try again!'
            
        return render_template('index.html', language=language, ispost=isPost, code=code, error=error, fileDown=fileName)

if __name__ == '__main__':
    app.run(debug=True)
