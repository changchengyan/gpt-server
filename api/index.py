from flask import Flask, request, jsonify,send_from_directory
from requests import HTTPError
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

from utils import utils

from utils  import getFileData

load_dotenv()

app = Flask(__name__,static_folder='dist')
@app.route('/')
def index():
    return app.send_static_file('index.html')


# 设置上传文件的保存目录
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/api/content', methods=['POST'])
def upload_files():

    print(request.files)
    print(len(request.files))

    print(request.form)

    try:

        if request.form["token"] is None or request.form["model"] == '':
            return jsonify({'code':500,'message': 'not token'}), 200

        if 'file' not in request.files and not 'text' in request.form:
            return jsonify({'code':500,'message': 'not file or text'}), 200
        
        text =  request.form['text']
        api_key = request.form["token"]
        model = request.form["model"]

        if 'file'  in request.files:
            promot =  request.form['text']
            if not promot:
                return jsonify({'code':500,'message': 'not file or text'}), 200
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'code':500,'message': 'no file  upload', 'data': None}), 200
            file = request.files['file']
            file_path = ""
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)

            res = getFileData.getFileData(filePaths=[file_path],promot=promot,api_key=api_key,model=model)

            return jsonify({"code":200,'message': 'fetch Success', 'data': res}), 200
        
        else:
            text =  request.form['text']
            print(text)
            res = utils.fetch_text_bychatgpt(text,api_key=api_key,model=model)
            return jsonify({"code":200,'message': 'fetch Success', 'data': res}), 200
        
    except HTTPError as error:
            return jsonify({"code":500,'message': error, 'data': None}), 200    

