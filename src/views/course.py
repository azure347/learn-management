from flask import Blueprint, request, session, jsonify
from src.util.db import DBHandler
from src.util.interceptor import is_instructor, is_student
from src.util.common import Page
import datetime

course_view = Blueprint('course_view', __name__, url_prefix='/course')


# 查询进行中的课程
@course_view.route('/having', methods=['GET'])
def having():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) AS total_count from course c inner join user u on c.instructor_id = u.id where c.start_date <= CURDATE() and c.end_date >= CURDATE() and c.state = 1 and u.role = "instructor" and u.`status` = 1 and u.state = 1 and (c.course_name like %s or u.username like %s)',
        args=(search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/having?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select c.course_name,u.username,DATE_FORMAT(c.start_date, "%Y-%m-%d") AS start_date,DATE_FORMAT(c.end_date, "%Y-%m-%d") AS end_date from course c inner join user u on c.instructor_id = u.id where c.start_date <= CURDATE() and c.end_date >= CURDATE() and c.state = 1 and u.role = "instructor" and u.`status` = 1 and u.state = 1 and (c.course_name like %s or u.username like %s) limit %s,%s',
        args=(search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 查询未开课的课程
@course_view.route('/nostart', methods=['GET'])
def nostart():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='select count(*) as total_count from course where start_date > CURDATE() and state = 1 and course_name like %s',
        args=(search_query,)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/having?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select course_name,DATE_FORMAT(start_date, "%Y-%m-%d") AS start_date from course where start_date > CURDATE() and state = 1 and course_name like %s limit %s,%s',
        args=(search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 分页查询课程列表
@course_view.route('/all', methods=['GET'])
def all():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from course c inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' where c.state = 1 and (c.course_name like %s or u.username like %s or c.course_description like %s)",
        args=(search_query, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/all?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select c.id,c.course_name,u.username,c.course_description,DATE_FORMAT(c.start_date, '%Y-%m-%d') AS start_date,DATE_FORMAT(c.end_date, '%Y-%m-%d') AS end_date from course c inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' where c.state = 1 and (c.course_name like %s or u.username like %s or c.course_description like %s) limit %s,%s",
        args=(search_query, search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 根据id查询课程详情
@course_view.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    course = DBHandler().query(
        sql="select id,course_name,instructor_id,course_description,DATE_FORMAT(start_date, '%Y-%m-%d') AS start_date,DATE_FORMAT(end_date, '%Y-%m-%d') AS end_date from course where state = 1 and id = %s",
        args=(id,)
    )
    DBHandler().close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course': course}})


# 添加课程
@course_view.route('/add', methods=['POST'])
def add():
    course_name = request.get_json().get('course_name')
    instructor_id = request.get_json().get('instructor_id')
    course_description = request.get_json().get('course_description')
    start_date = request.get_json().get('start_date')
    end_date = request.get_json().get('end_date')
    if not course_name or not instructor_id or not course_description or not start_date or not end_date:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    res = db.exec(
        sql='insert into course(course_name,instructor_id,course_description,start_date,end_date) values(%s,%s,%s,%s,%s)',
        args=(course_name, instructor_id, course_description, start_date, end_date)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '添加成功'})


# 修改课程
@course_view.route('/update', methods=['POST'])
def update():
    id = request.get_json().get('id')
    course_name = request.get_json().get('course_name')
    instructor_id = request.get_json().get('instructor_id')
    course_description = request.get_json().get('course_description')
    start_date = request.get_json().get('start_date')
    end_date = request.get_json().get('end_date')
    print(id, course_name, instructor_id, course_description, start_date, end_date)
    if not id or not course_name or not instructor_id or not course_description or not start_date or not end_date:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='update course set course_name = %s,instructor_id = %s,course_description = %s,start_date = %s,end_date = %s where id = %s',
        args=(course_name, instructor_id, course_description, start_date, end_date, id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '修改成功'})


# 删除课程
@course_view.route('/delete', methods=['POST'])
def delete():
    id = request.get_json().get('id')
    if not id:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    # 已开课的课程无法删除
    res = db.query(
        sql='select * from course where state = 1 and id = %s',
        args=(id,)
    )
    if res['start_date'] < datetime.date.today() < res['end_date']:
        return jsonify({'code': 400, 'msg': '已开课的课程无法删除'})
    db.exec(
        sql='update course set state = 0 where id = %s',
        args=(id,)
    )
    # 删除学生选课数据
    db.exec(
        sql='update student_course set state = 0 where course_id = %s',
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})


# 分页查询教师的课程列表
@course_view.route('/by-instructor-id', methods=['GET'])
@is_instructor
def by_instructor_id():
    instructor_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='SELECT count(*) as total_count from course where state = 1 and instructor_id = %s and course_name like %s',
        args=(instructor_id, search_query)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/by-instructor-id?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='SELECT id,course_name,DATE_FORMAT(start_date, "%Y-%m-%d") as start_date,DATE_FORMAT(end_date, "%Y-%m-%d") as end_date from course where state = 1 and instructor_id = %s and course_name like %s limit %s,%s',
        args=(instructor_id, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 分页查询课程的学生信息
@course_view.route('/by-instructor-id-stu', methods=['GET'])
@is_instructor
def by_instructor_id_stu():
    instructor_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='SELECT count(*) as total_count from course where state = 1 and instructor_id = %s and course_name like %s',
        args=(instructor_id, search_query)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/by-instructor-id-stu?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='select c.id,c.course_name,student_num from course c left join (select course_id,count(*) as student_num from student_course where state = 1 and `status` = 1 GROUP BY course_id) sc on c.id = sc.course_id where c.state = 1 and instructor_id = %s and c.course_name like %s limit %s,%s',
        args=(instructor_id, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})


# 分页查询课程的学生提交作业列表
@course_view.route('/assignment-submit', methods=['GET'])
@is_instructor
def assignment_submit():
    course_id = request.args.get('course_id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    db = DBHandler()
    # 查询课程信息
    course = db.query(
        sql='select * from course where id = %s and state = 1',
        args=(course_id,)
    )
    count = db.query(
        sql='SELECT count(*) as total_count from student_assignment sa inner join assignment a on sa.assignment_id = a.id and a.state = 1 inner join user u on sa.student_id = u.id and u.state = 1 and u.`status` = 1 where sa.state = 1 and sa.`status` in (1,2) and sa.assignment_id in (select id from assignment where state = 1 and course_id = %s)',
        args=(course_id,)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/assignment-submit?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql='SELECT sa.id,a.assignment_name,u.username from student_assignment sa inner join assignment a on sa.assignment_id = a.id and a.state = 1 inner join user u on sa.student_id = u.id and u.state = 1 and u.`status` = 1 where sa.state = 1 and sa.`status` in (1,2) and sa.assignment_id in (select id from assignment where state = 1 and course_id = %s) limit %s,%s',
        args=(course_id, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify(
        {'code': 200, 'msg': '查询成功', 'data': {'sa_list': res, 'course_name': course['course_name'], 'pages': pages}})


# 查询当前登录学生可选的课程列表
@course_view.route('/select', methods=['GET'])
@is_student
def select():
    student_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from course c inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' left join student_course sc on c.id = sc.course_id and sc.student_id = %s and sc.state = 1 and sc.`status` = 0 where c.state = 1 and c.start_date > CURDATE() and c.id not in (select course_id from student_course where student_id = %s and `status` = 1 and state = 1) and (c.course_name like %s or u.username like %s)",
        args=(student_id, student_id, search_query, search_query)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/course/select?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select c.id,c.course_name,u.username,DATE_FORMAT(c.start_date, '%Y-%m-%d') as start_date,DATE_FORMAT(c.end_date, '%Y-%m-%d') as end_date,ifnull(sc.`status`, -1) as `status` from course c inner join user u on c.instructor_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'instructor' left join student_course sc on c.id = sc.course_id and sc.student_id = %s and sc.state = 1 and sc.`status` = 0 where c.state = 1 and c.start_date > CURDATE() and c.id not in (select course_id from student_course where student_id = %s and `status` = 1 and state = 1) and (c.course_name like %s or u.username like %s) limit %s,%s",
        args=(student_id, student_id, search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify(
        {'code': 200, 'msg': '查询成功', 'data': {'course_list': res, 'pages': pages}})
