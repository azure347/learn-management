from flask import Blueprint, request, jsonify, session
from src.util.db import DBHandler
from src.util.interceptor import is_admin, is_student
from src.util.common import Page
import datetime

student_course_view = Blueprint('student_course_view', __name__, url_prefix='/student-course')


# 查询学生选课分页列表
@student_course_view.route('/select', methods=['GET'])
@is_admin
def select():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from student_course sc inner join user u on sc.student_id = u.id and u.state = 1 and u.`status` = 1 and u.role = "student" inner join course c on sc.course_id = c.id and c.state = 1 where sc.state = 1 and (c.course_name like %s or u.username like %s)',
        args=(search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-course/select?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select sc.id,c.course_name,DATE_FORMAT(c.start_date, "%Y-%m-%d") AS start_date,DATE_FORMAT(c.end_date, "%Y-%m-%d") AS end_date,u.username,sc.`status` from student_course sc inner join user u on sc.student_id = u.id and u.state = 1 and u.`status` = 1 and u.role = "student" inner join course c on sc.course_id = c.id and c.state = 1 where sc.state = 1 and (c.course_name like %s or u.username like %s) limit %s,%s',
        args=(search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'student_course_list': res, 'pages': pages}})


# 通过学生的选课
@student_course_view.route('/select-pass', methods=['GET'])
@is_admin
def select_pass():
    student_course_id = request.args.get('id')
    db = DBHandler()
    course_date = db.query(
        sql='select c.start_date,c.end_date from student_course sc inner join course c on sc.course_id = c.id and c.state = 1 where sc.state = 1 and sc.`status` = 0 and sc.id = %s',
        args=(student_course_id,))
    print(course_date)
    # 判断课程是否开始或结束，只能通过未开课的课程
    if course_date['start_date'] < datetime.date.today():
        return jsonify({'code': 400, 'msg': '课程已开课，无法通过'})
    if course_date['end_date'] < datetime.date.today():
        return jsonify({'code': 400, 'msg': '课程已结束，无法通过'})
    db.exec(
        sql='update student_course set `status` = 1 where state = 1 and id = %s',
        args=(student_course_id,))
    db.close()
    return jsonify({'code': 200, 'msg': '选课通过'})


# 删除学生选课
@student_course_view.route('/delete', methods=['GET'])
@is_admin
def delete():
    student_course_id = request.args.get('id')
    print(student_course_id)
    db = DBHandler()
    res = db.query(
        sql='select sc.`status`,c.start_date,c.end_date from student_course sc inner join course c on sc.course_id = c.id and c.state = 1 where sc.state = 1 and sc.id = %s',
        args=(student_course_id,)
    )
    # 已通过的课程在开课期间无法删除
    if res['status'] == 1 and res['start_date'] < datetime.date.today() < res['end_date']:
        return jsonify({'code': 400, 'msg': '已通过的申请在开课期间无法删除'})
    db.exec(
        sql='update student_course set state = 0 where state = 1 and id = %s',
        args=(student_course_id,))
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})


# 查询当前登录的学生的课程列表
@student_course_view.route('/by-student-id', methods=['GET'])
@is_student
def by_student_id():
    student_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from student_course sc inner join course c on sc.course_id = c.id and c.state = 1 inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = "instructor" where sc.state = 1 and sc.`status` = 1 and student_id = %s and (c.course_name like %s or u.username like %s)',
        args=(student_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-course/my?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select sc.id,sc.course_id,c.instructor_id,c.course_name,u.username as instructor_name,DATE_FORMAT(c.start_date, "%Y-%m-%d") AS start_date,DATE_FORMAT(c.end_date, "%Y-%m-%d") AS end_date from student_course sc inner join course c on sc.course_id = c.id and c.state = 1 inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = "instructor" where sc.state = 1 and sc.`status` = 1 and student_id = %s and (c.course_name like %s or u.username like %s) limit %s,%s',
        args=(student_id, search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 学生选课
@student_course_view.route('/choose', methods=['GET'])
@is_student
def choose():
    student_id = session.get('user').get('id')
    course_id = request.args.get('course_id')
    db = DBHandler()
    course_date = db.query(
        sql='select start_date, end_date from course where state = 1 and id = %s',
        args=(course_id,)
    )
    print(course_date)
    # 判断课程是否开始或结束，只能通过未开课的课程
    if course_date['start_date'] < datetime.date.today():
        return jsonify({'code': 400, 'msg': '课程已开课，无法选择'})
    if course_date['end_date'] < datetime.date.today():
        return jsonify({'code': 400, 'msg': '课程已结束，无法选择'})
    db.exec(
        sql='insert into student_course(student_id,course_id) values(%s,%s)',
        args=(student_id, course_id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '选择成功'})
