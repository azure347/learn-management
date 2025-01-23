from flask import Blueprint, request, jsonify, send_from_directory
import os
import uuid

file_view = Blueprint('file', __name__, url_prefix='/file')

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')


# 文件上传
@file_view.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(path):
        os.makedirs(path)
    f = request.files.get('file')
    filename = str(uuid.uuid4()).replace('-', '') + '.' + f.filename.split('.')[1]
    f.save(os.path.join(path, filename))
    return jsonify({'code': 200, 'msg': '上传成功', 'data': {'filename': filename}})


# 文件下载
@file_view.route('/get/<filename>', methods=['GET'])
def get(filename):
    return send_from_directory(path, filename, as_attachment=True)
