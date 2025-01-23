from flask import Blueprint, request, session, jsonify
from src.util.db import DBHandler
from src.util.interceptor import is_instructor, is_student
from src.util.common import Page

student_assignment_view = Blueprint('student_assignment_view', __name__, url_prefix='/student-assignment')


# 查询作业详情
@student_assignment_view.route('/detail', methods=['GET'])
def detail():
    id = request.args.get('id')
    db = DBHandler()
    res = db.query(
        sql="select sa.id,sa.student_id,u.username,sa.assignment_id,a.assignment_name,a.assignment_requirement,sa.file_name,sa.score,sa.feedback,sa.`status` from student_assignment sa inner join user u on sa.student_id = u.id and u.state = 1 and u.`status` = 1 and u.role = 'student' inner join assignment a on sa.assignment_id = a.id and a.state = 1 where sa.state = 1 and sa.id = %s",
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'stu_assignment': res}})


# 教师批改作业
@student_assignment_view.route('/correct', methods=['POST'])
@is_instructor
def correct():
    db = DBHandler()
    data = request.get_json()
    id = data.get('id')
    score = data.get('score')
    feedback = data.get('feedback')
    db.exec(
        sql="update student_assignment set score = %s, feedback = %s, `status` = 2 where id = %s and state = 1",
        args=(score, feedback, id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '批改成功'})


# 分页查询当前登录学生的未提交的作业列表
@student_assignment_view.route('/unfinished', methods=['GET'])
@is_student
def unfinished():
    student_id = session.get('user').get('id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from student_assignment sa inner join assignment a on sa.assignment_id = a.id and a.state = 1 inner join course c on a.course_id = c.id and c.state = 1 where sa.student_id = %s and sa.`status` = 0 and sa.state = 1 and (a.assignment_name like %s or c.course_name like %s)",
        args=(student_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-assignment/unfinished?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select sa.id,a.assignment_name,c.course_name,DATE_FORMAT(a.submit_deadline_time, '%Y-%m-%d %H:%i:%S') AS submit_deadline_time from student_assignment sa inner join assignment a on sa.assignment_id = a.id and a.state = 1 inner join course c on a.course_id = c.id and c.state = 1 where sa.student_id = %s and sa.`status` = 0 and sa.state = 1 and (a.assignment_name like %s or c.course_name like %s) limit %s,%s",
        args=(student_id, search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})


# 分页查询当前登录学生的某一课程的作业分数列表
@student_assignment_view.route('/by-course-score', methods=['GET'])
@is_student
def by_course_score():
    student_id = session.get('user').get('id')
    course_id = request.args.get('course_id')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` = 2 where a.state = 1 and a.course_id = %s and (a.assignment_name like %s or sa.score like %s)",
        args=(student_id, course_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-assignment/by-course-score?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select sa.id,a.assignment_name,sa.score from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` = 2 where a.state = 1 and a.course_id = %s and (a.assignment_name like %s or sa.score like %s) limit %s,%s",
        args=(student_id, course_id, search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})


# 查询当前登录学生的某一课程的作业情况统计
@student_assignment_view.route('/by-course-status-count', methods=['GET'])
def by_course_status_count():
    student_id = session.get('user').get('id')
    course_id = request.args.get('course_id')
    print(course_id)
    db = DBHandler()
    res = db.query(
        sql="select `status`,count(id) as count from student_assignment where state = 1 and student_id = %s and assignment_id in (select id from assignment where course_id = %s and state = 1) group by `status`",
        args=(student_id, course_id),
        one=False
    )
    db.close()
    no_do = 0
    do = 0
    if res:
        for i in range(len(res)):
            if res[i]['status'] == 0:
                no_do = res[i]['count']
            else:
                do = do + res[i]['count']
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'no_complete': no_do, 'complete': do}})


# 查询当前登录学生的某一课程的未完成作业列表
@student_assignment_view.route('/unfinished-by-course', methods=['GET'])
@is_student
def unfinished_by_course():
    student_id = session.get('user').get('id')
    course_id = request.args.get('course_id')
    print(course_id)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` = 0 where a.state = 1 and a.course_id = %s and (a.assignment_name like %s or a.assignment_requirement like %s)",
        args=(student_id, course_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-assignment/unfinished-by-course?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select sa.id,a.id as assignment_id,a.assignment_name,a.assignment_requirement,DATE_FORMAT(a.submit_deadline_time,'%Y-%m-%d %H:%i:%S') AS submit_deadline_time,a.file_name from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` = 0 where a.state = 1 and a.course_id = %s and (a.assignment_name like %s or a.assignment_requirement like %s) limit %s,%s",
        args=(student_id, course_id, search_query, search_query, offset, page_size),
        one=False
    )
    print('-------------------', res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})


# 学生提交作业
@student_assignment_view.route('/submit', methods=['POST'])
@is_student
def submit():
    id = request.get_json().get('id')
    file_name = request.get_json().get('file_name')
    if not id or not file_name:
        return jsonify({'code': 400, 'msg': '参数错误'})
    db = DBHandler()
    db.exec(
        sql='update student_assignment set file_name = %s,`status` = 1 where id = %s and state = 1',
        args=(file_name, id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '提交成功'})


# 查询当前登录学生的某一课程完成的作业列表
@student_assignment_view.route('/finished-by-course', methods=['GET'])
@is_student
def finished_by_course():
    student_id = session.get('user').get('id')
    course_id = request.args.get('course_id')
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    print(course_id)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` in (1,2) where a.state = 1 and a.course_id = %s and a.assignment_name like %s",
        args=(student_id, course_id, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/student-assignment/finished-by-course?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select sa.id,sa.assignment_id,a.assignment_name,sa.file_name,sa.score,sa.feedback,sa.`status` from assignment a inner join student_assignment sa on a.id = sa.assignment_id and sa.student_id = %s and sa.state = 1 and sa.`status` in (1,2) where a.state = 1 and a.course_id = %s and a.assignment_name like %s limit %s,%s",
        args=(student_id, course_id, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})
