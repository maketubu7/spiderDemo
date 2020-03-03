# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 17:15
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : emailServer.py
# @Software: PyCharm

from flask import Flask,redirect,url_for,jsonify
import platform,os
from flask import request,jsonify,render_template
import json,uuid
from werkzeug.utils import secure_filename
from webDemo.common.logUtil import logUtil
from webDemo.common.emailUtil import emailUtil



if platform.system() == "Windows":
    slash = '\\'
if platform.system()=="Linux":
    slash = '/'

app = Flask(__name__)

app.config.from_pyfile("app_config.py")

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('send_email.html')

@app.route('/send_email',methods=['GET','POST'])
def send_email():
    resp = {'code':200,'msg':'操作成功','data':{}}
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        filenames = []

        for file in files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            filenames.append(filename)
        req = request.values
        user_address = req["user_address"] if 'user_address' in req else ''
        to_address = req["to_address"].split(',') if 'to_address' in req else ''
        password = req["password"] if 'password' in req else ''
        header = req["header"] if 'header' in req else ''
        content = req["content"] if 'content' in req else ''
        email = emailUtil(user_address,password)
        for filename in filenames:
            email.add_attachment(filename)
        email.send_email(to_address,header,content)
        return jsonify(resp)
    resp['msg'] = '操作失败'
    return jsonify(resp)

if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.run(host='127.0.0.1',port=1111)


