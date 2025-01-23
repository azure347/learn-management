from flask import Blueprint, request, jsonify, session
from src.util.db import DBHandler
from src.util.common import Page
from src.util.interceptor import is_admin
import datetime

lecture_view = Blueprint('lecture_view', __name__, url_prefix='/lecture')


# 获取全部讲座列表
@lecture_view.route('/all', methods=['GET'])
def all():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    print("search: ", search_query)
    db = DBHandler()
    count = db.query(
        sql="SELECT count(*) as total_count from lecture l INNER JOIN user u on l.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' where l.state = 1 and (l.lecture_name like %s or l.lecture_description like %s)",
        args=(search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/lecture/all?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="SELECT l.id,l.lecture_name,u.username,DATE_FORMAT(l.lecture_start_time, '%Y-%m-%d %H:%i:%S') as lecture_start_time,DATE_FORMAT(l.lecture_end_time, '%Y-%m-%d %H:%i:%S') as lecture_end_time,l.lecture_description,l.file_name,l.`status`,DATE_FORMAT(l.create_time, '%Y-%m-%d %H:%i:%S') as create_time from lecture l INNER JOIN user u on l.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' where l.state = 1 and (l.lecture_name like %s or l.lecture_description like %s) limit %s,%s",
        args=(search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'lecture_list': res, 'pages': pages}})


# 通过讲师的讲座申请
@lecture_view.route('/apply', methods=['GET'])
@is_admin
def apply():
    id = request.args.get('id')
    db = DBHandler()
    lecture_date = db.query(
        sql='select lecture_start_time,lecture_end_time from lecture where state = 1 and id = %s',
        args=(id,)
    )
    # 判断讲座是否过期
    if lecture_date['lecture_start_time'] > datetime.datetime.now():
        # 可以通过
        db.exec(
            sql='update lecture set `status` = 1 where id = %s',
            args=(id,)
        )
        db.close()
        return jsonify({'code': 200, 'msg': '通过申请'})
    else:
        db.close()
        return jsonify({'code': 400, 'msg': '讲座已过期'})


# 删除讲师讲座
@lecture_view.route('/delete', methods=['GET'])
def delete():
    id = request.args.get('id')
    db = DBHandler()
    res = db.query(
        sql='select lecture_start_time,lecture_end_time,`status` from lecture where state = 1 and id = %s',
        args=(id,)
    )
    if res['status'] == 1 and res['lecture_start_time'] < datetime.datetime.now() < res['lecture_end_time']:
        return jsonify({'code': 400, 'msg': '讲座正在进行中，无法删除'})
    db.exec(
        sql='update lecture set state = 0 where id = %s',
        args=(id,)
    )
    # 删除关联表数据
    db.exec(
        sql='update student_lecture set state = 0 where lecture_id = %s',
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})


# 分页查询我的讲座列表
@lecture_view.route('/my-lecture-list', methods=['GET'])
def my_lecture_list():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    user_id = session.get('user').get('id')
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from lecture where state = 1 and instructor_id = %s and (lecture_name like %s or lecture_description like %s)",
        args=(user_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/lecture/my-lecture-list?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select id,lecture_name,DATE_FORMAT(lecture_start_time, '%Y-%m-%d %H:%i') as lecture_start_time,DATE_FORMAT(lecture_end_time, '%Y-%m-%d %H:%i') as lecture_end_time,lecture_description,file_name,`status` from lecture where state = 1 and instructor_id = %s and (lecture_name like %s or lecture_description like %s) limit %s,%s",
        args=(user_id, search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'lecture_list': res, 'pages': pages}})


# 根据id查询讲座详情
@lecture_view.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    db = DBHandler()
    res = db.query(
        sql="select id,lecture_name,DATE_FORMAT(lecture_start_time, '%Y-%m-%d %H:%i') as lecture_start_time,DATE_FORMAT(lecture_end_time, '%Y-%m-%d %H:%i') as lecture_end_time,lecture_description,file_name,`status` from lecture where state = 1 and id = %s",
        args=(id,)
    )
    user_ids = []
    user_ids = db.query(
        sql='SELECT student_id FROM student_lecture WHERE state = 1 AND lecture_id = %s',
        args=(id,),
        one=False
    )
    user_ids = [user_id['student_id'] for user_id in user_ids]
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'lecture': res, 'user_ids': user_ids}})


# 添加讲座
@lecture_view.route('/add', methods=['POST'])
def add():
    user_id = session.get('user').get('id')
    lecture_name = request.get_json().get('lecture_name')
    lecture_description = request.get_json().get('lecture_description')
    lecture_start_time = request.get_json().get('lecture_start_time')
    lecture_end_time = request.get_json().get('lecture_end_time')
    file_name = request.get_json().get('file_name')
    user_ids = request.get_json().get('user_list')
    if not user_id or not lecture_name or not lecture_description or not lecture_start_time or not lecture_end_time or not file_name:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='insert into lecture(instructor_id,lecture_name,lecture_description,lecture_start_time,lecture_end_time,file_name) values(%s,%s,%s,%s,%s,%s)',
        args=(user_id, lecture_name, lecture_description, lecture_start_time, lecture_end_time, file_name)
    )
    lecture_id = db.get_insert_id()
    # 添加关联表数据
    rows = [(lecture_id, user_id) for user_id in user_ids]
    db.exec(
        sql='INSERT INTO student_lecture (lecture_id, student_id) VALUES (%s, %s)',
        args=rows,
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '添加成功'})


# 修改讲座
@lecture_view.route('/update', methods=['POST'])
def update():
    id = request.get_json().get('id')
    lecture_name = request.get_json().get('lecture_name')
    lecture_description = request.get_json().get('lecture_description')
    lecture_start_time = request.get_json().get('lecture_start_time')
    lecture_end_time = request.get_json().get('lecture_end_time')
    file_name = request.get_json().get('file_name')
    user_ids = request.get_json().get('user_list')
    status = 0
    if not id or not lecture_name or not lecture_description or not lecture_start_time or not lecture_end_time or not file_name:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='update lecture set lecture_name = %s,lecture_description = %s,lecture_start_time = %s,lecture_end_time = %s,file_name = %s,status = %s where state = 1 and id = %s',
        args=(lecture_name, lecture_description, lecture_start_time, lecture_end_time, file_name, status, id)
    )
    # 删除关联表数据
    db.exec(sql='UPDATE student_lecture set state = 0 WHERE lecture_id = %s', args=(id,))
    # 添加关联表数据
    rows = [(id, user_id) for user_id in user_ids]
    db.exec(
        sql='INSERT INTO student_lecture (lecture_id, student_id) VALUES (%s, %s)',
        args=rows,
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '修改成功'})
