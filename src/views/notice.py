from flask import Blueprint, request, session, jsonify
from src.util.db import DBHandler
from src.util.common import Page
from src.util.interceptor import is_instructor

notice_view = Blueprint('notice_view', __name__, url_prefix='/notice')


# 添加通知
@notice_view.route('/add', methods=['POST'])
def add():
    user_id = session.get('user').get('id')
    notice_name = request.get_json().get('notice_name')
    notice_content = request.get_json().get('notice_content')
    file_name = request.get_json().get('file_name')
    type = request.get_json().get('notice_type')
    user_ids = request.get_json().get('user_list')
    db = DBHandler()
    db.exec(
        sql='insert into notice(notice_name,notice_content,file_name,user_id,type) values(%s,%s,%s,%s,%s)',
        args=(notice_name, notice_content, file_name, user_id, type)
    )
    notice_id = db.get_insert_id()
    if notice_id:
        if type == 2 and user_ids and len(user_ids) > 0:
            # 添加关联表数据
            rows = [(notice_id, user_id) for user_id in user_ids]
            db.exec(
                sql='INSERT INTO user_notice (notice_id, user_id) VALUES (%s, %s)',
                args=rows,
                one=False
            )
        db.close()
        return jsonify({'code': 200, 'msg': '添加成功'})
    else:
        return jsonify({'code': 500, 'msg': '添加失败'})


# 修改通知
@notice_view.route('/update', methods=['POST'])
def update():
    user_id = session.get('user').get('id')
    id = request.get_json().get('id')
    notice_name = request.get_json().get('notice_name')
    notice_content = request.get_json().get('notice_content')
    file_name = request.get_json().get('file_name')
    type = request.get_json().get('notice_type')
    user_ids = request.get_json().get('user_list')
    db = DBHandler()
    db.exec(
        sql='UPDATE notice set user_id = %s,notice_name = %s,notice_content = %s,file_name = %s,type = %s WHERE id = %s',
        args=(user_id, notice_name, notice_content, file_name, type, id)
    )
    # 删除关联表数据
    db.exec(sql='UPDATE user_notice set state = 0 WHERE notice_id = %s', args=(id,))
    # 添加关联表数据
    if type == 2 and user_ids and len(user_ids) > 0:
        rows = [(id, user_id) for user_id in user_ids]
        db.exec(
            sql='INSERT INTO user_notice (notice_id, user_id) VALUES (%s, %s)',
            args=rows,
            one=False
        )
    db.close()
    return jsonify({'code': 200, 'msg': '更新成功'})


# 删除通知
@notice_view.route('/delete', methods=['POST'])
def delete():
    id = request.get_json().get('id')
    print(id)
    db = DBHandler()
    db.exec(
        sql='update notice set state = 0 where id = %s',
        args=(id,)
    )
    db.exec(
        sql='update user_notice set state = 0 where notice_id = %s',
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})


# 根据id查询单个通知
@notice_view.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    db = DBHandler()
    notice = db.query(
        sql='SELECT id,user_id,notice_name,notice_content,file_name,type FROM notice WHERE state = 1 and id = %s',
        args=(id,)
    )
    user_ids = []
    if notice['type'] == 2:
        # 查询关联用户id
        user_ids = db.query(
            sql='SELECT user_id FROM user_notice WHERE state = 1 AND notice_id = %s',
            args=(id,),
            one=False
        )
        user_ids = [user_id['user_id'] for user_id in user_ids]
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice': notice, 'user_ids': user_ids}})


# 获取公共通知列表
@notice_view.route('/list', methods=['GET'])
def list():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and n.type = 1 and (n.notice_name like %s or n.notice_content like %s)',
        args=(search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/notice/list?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select n.id,n.notice_name,n.notice_content,n.file_name,DATE_FORMAT(n.create_time, "%Y-%m-%d %H:%i:%S") AS create_time,u.username from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and n.type = 1 and (n.notice_name like %s or n.notice_content like %s) limit %s,%s',
        args=(search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice_list': res, 'pages': pages}})


# 获取全部通知列表
@notice_view.route('/all', methods=['GET'])
def all():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and (n.notice_name like %s or n.notice_content like %s)',
        args=(search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/notice/all?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select n.id,n.notice_name,n.notice_content,n.file_name,n.type,DATE_FORMAT(n.create_time, "%Y-%m-%d %H:%i:%S") AS create_time,u.username from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and (n.notice_name like %s or n.notice_content like %s) limit %s,%s',
        args=(search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice_list': res, 'pages': pages}})


# 分页查询当前用户收到的通知列表
@notice_view.route('/list-by-user-receive', methods=['GET'])
def list_by_user_receive():
    user_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and (n.notice_name like %s or n.notice_content like %s) and (n.type = 1 or n.id in (select notice_id from user_notice where state = 1 and user_id = %s))',
        args=(search_query, search_query, user_id,)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/notice/list-by-user-receive?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select n.id,n.notice_name,n.notice_content,n.file_name,n.type,DATE_FORMAT(n.create_time, "%Y-%m-%d %H:%i:%S") AS create_time,u.username from notice n inner join user u on n.user_id = u.id and u.`status` = 1 and u.state = 1 where n.state = 1 and (n.notice_name like %s or n.notice_content like %s) and (n.type = 1 or n.id in (select notice_id from user_notice where state = 1 and user_id = %s)) limit %s,%s',
        args=(search_query, search_query, user_id, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice_list': res, 'pages': pages}})


# 分页查询当前用户收到的指定通知人的通知列表
@notice_view.route('/list-by-send-user', methods=['GET'])
def list_by_send_user():
    user_id = session.get('user').get('id')
    send_user_id = request.args.get('send_user_id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from notice where user_id = %s and state = 1 and (type = 1 or id in (select un.notice_id from user_notice un inner join notice n on un.notice_id = n.id and n.user_id=%s and n.state = 1 and n.type = 2 where un.state = 1 and un.user_id = %s)) and (notice_name like %s or notice_content like %s)',
        args=(send_user_id, send_user_id, user_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/notice/list-by-send-user?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select id,notice_name,notice_content,file_name,type,DATE_FORMAT(create_time, "%Y-%m-%d %H:%i:%S") AS create_time from notice where user_id = %s and state = 1 and (type = 1 or id in (select un.notice_id from user_notice un inner join notice n on un.notice_id = n.id and n.user_id=%s and n.state = 1 and n.type = 2 where un.state = 1 and un.user_id = %s)) and (notice_name like %s or notice_content like %s) limit %s,%s',
        args=(send_user_id, send_user_id, user_id,search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice_list': res, 'pages': pages}})


# 获取当前登录用户发布的通知列表
@notice_view.route('/list-by-user', methods=['GET'])
@is_instructor
def list_by_user():
    user_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from notice where state = 1 and user_id = %s and (notice_name like %s or notice_content like %s)',
        args=(user_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/notice/list-by-user?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select id,notice_name,notice_content,file_name,type,DATE_FORMAT(create_time, "%Y-%m-%d %H:%i:%S") AS create_time from notice where state = 1 and user_id = %s and (notice_name like %s or notice_content like %s) limit %s,%s',
        args=(user_id, search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'notice_list': res, 'pages': pages}})
