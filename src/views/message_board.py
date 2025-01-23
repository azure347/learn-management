from flask import Blueprint, request, session, jsonify
from src.util.db import DBHandler
from src.util.common import Page
from src.util.interceptor import is_student

message_board_view = Blueprint('message_board_view', __name__, url_prefix='/message-board')


# 分页查询学生留言列表
@message_board_view.route('/list', methods=['GET'])
def list():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from message_board mb inner join user u on mb.user_id = u.id and u.state = %s and u.`status` = %s and u.role = %s where mb.state = %s and (mb.message_content like %s or u.username like %s)",
        args=(1, 1, 'student', 1, search_query, search_query)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/message-board/list?page='
    }
    pages = Page(page_params)
    offset = (page - 1) * page_size
    res = db.query(
        sql="select mb.id,mb.user_id,mb.message_content,u.username,DATE_FORMAT(mb.update_time, '%Y-%m-%d %H:%i:%S') AS update_time from message_board mb inner join user u on mb.user_id = u.id and u.state = %s and u.`status` = %s and u.role = %s where mb.state = %s and (mb.message_content like %s or u.username like %s) order by mb.update_time desc limit %s,%s",
        args=(1, 1, 'student', 1, search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'message_board_list': res, 'pages': pages}})


# 学生发送留言
@message_board_view.route('/add', methods=['POST'])
@is_student
def add():
    message_content = request.json.get('message_content')
    user_id = session.get('user').get('id')
    if not message_content:
        return jsonify({'code': 400, 'msg': '留言内容不能为空'})
    db = DBHandler()
    db.exec(
        sql="insert into message_board (user_id,message_content) values (%s,%s)",
        args=(user_id, message_content)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '留言成功'})


# 学生删除留言
@message_board_view.route('/delete', methods=['GET'])
@is_student
def delete():
    id = request.args.get('id')
    user_id = session.get('user').get('id')
    if not id:
        return jsonify({'code': 400, 'msg': '留言id不能为空'})
    db = DBHandler()
    db.exec(
        sql="update message_board set state = %s where id = %s and user_id = %s",
        args=(0, id, user_id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})
