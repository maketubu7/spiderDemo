# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 17:15
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : webServer.py
# @Software: PyCharm
from flask import Flask,redirect,url_for,jsonify
import platform,os
from flask import request,jsonify,render_template
import json,uuid
from werkzeug.utils import secure_filename
from webDemo.common.logUtil import logUtil



if platform.system() == "Windows":
    slash = '\\'
if platform.system()=="Linux":
    slash = '/'

app = Flask(__name__)

# @app.route('/',methods=["GET","POST"])
# def index():
#     req = request.values
#     # resp = {"code":"200", "msg":"success","data":{}}
#     resp = {"name":"网络编程基础", "xm":"make","url":"http://127.0.0.1:1111"}
#     v = req["v"] if "v" in req else '666'
#     res = [resp,resp,resp]
#     # return jsonify(res)
#     return render_template('domDemo.html')

app.config.from_pyfile("app_config.py")
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
#判断文件夹是否存在，如果不存在则创建
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
else:
    pass
# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config["ALLOW_EXTENSIONS"]

@app.route('/login',methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route('/user',methods=["GET","POST"])
def user():
    return render_template('user.html')


@app.route('/upload',methods=["GET","POST"])
def upload():
    return render_template('upload.html')

@app.route('/deal_log',methods=["GET","POST"])
def deallog():
    resp = {"code":200,"msg":'操作成功',"data":{}}
    if request.method == 'POST':
        # 获取post过来的文件名称，从name=file参数中获取
        file = request.files['file']
        req = request.values
        usecols = req["usecols"].split(',') if "usecols" in req else [1]
        columns = req["columns"].split(',') if "columns" in req else ["phone"]
        drop_key = req["drop_key"].split(',') if "drop_key" in req else ["phone"]
        sep = req["sep"] if "sep" in req else ','
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文
            filename = secure_filename(file.filename)
            # 因为上次的文件可能有重名，因此使用uuid保存文件
            file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            file.save(filename)
            df = logUtil.deallog(filename=filename,usecols=usecols,columns=columns,drop_key=drop_key,sep=sep)
            logUtil.save_csv(df,filename)
            logUtil.save_mysql(df,'upload_log')
            data = df.to_dict(orient='list')
            resp["data"] = data
            return jsonify(resp)
    resp["code"] = 400
    resp["msg"] = '操作失败'
    return resp


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


if __name__ == '__main__':
    app.debug = True # 设置调试模式，生产模式的时候要关掉debug
    app.after_request(after_request)
    app.run(host='127.0.0.1',port=1111)


