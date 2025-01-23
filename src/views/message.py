from flask import Blueprint, request, jsonify, session
from src.util.db import DBHandler
from src.util.common import Page

message_view = Blueprint('message_view', __name__, url_prefix='/message')


# 发送消息
@message_view.route('/send', methods=['POST'])
def send_message():
    send_id = session.get('user').get('id')
    receive_id = request.json.get('receive_id')
    message = request.json.get('message')
    if send_id and receive_id and message:
        db = DBHandler()
        db.exec(sql='INSERT INTO message (send_id, receive_id, message_content) VALUES (%s, %s, %s)',
                args=(send_id, receive_id, message))
        db.close()
        return jsonify({'code': 200, 'msg': '消息发送成功'})
    else:
        return jsonify({'code': 400, 'msg': '参数错误'})


# 获取聊天记录
@message_view.route('/list', methods=['GET'])
def list():
    send_id = session.get('user').get('id')
    receive_id = request.args.get('receive_id')
    db = DBHandler()
    res = db.query(
        sql="select id,send_id,receive_id,message_content,DATE_FORMAT(create_time, '%Y-%m-%d %H:%i:%S') as create_time from message where state = 1 and send_id in (%s,%s) and receive_id in (%s,%s) order by create_time",
        args=(send_id, receive_id, send_id, receive_id),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'message_list': res}})
