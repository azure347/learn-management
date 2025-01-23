from flask import Blueprint, request, jsonify
from src.util.db import DBHandler
from src.util.common import Page

assignment_view = Blueprint('assignment_view', __name__, url_prefix='/assignment')


# 查询未完成作业的学生
@assignment_view.route('/unfinished', methods=['GET'])
def unfinished():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="SELECT count(*) as total_count from student_assignment stua inner join assignment a on stua.assignment_id = a.id AND a.state = 1 inner join course c on a.course_id = c.id AND c.state = 1 inner join user u on stua.student_id = u.id AND u.`status` = 1 AND u.state = 1 AND u.role = 'student' WHERE stua.`status` = 0 AND stua.state = 1 AND (u.username like %s OR c.course_name like %s OR a.assignment_name like %s)",
        args=(search_query, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/assignment/unfinished?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="SELECT u.username, c.course_name,a.assignment_name, DATE_FORMAT(a.submit_deadline_time, '%Y-%m-%d %H:%i:%S') AS submit_deadline_time FROM student_assignment sa INNER JOIN assignment a on sa.assignment_id = a.id AND a.state = 1 INNER JOIN course c on a.course_id = c.id AND c.state = 1 INNER JOIN user u on sa.student_id = u.id AND u.`status` = 1 AND u.state = 1 AND u.role = 'student' WHERE sa.`status` = 0 AND sa.state = 1 AND (u.username like %s OR c.course_name like %s OR a.assignment_name like %s) ORDER BY a.submit_deadline_time limit %s,%s",
        args=(search_query, search_query, search_query, offset, page_size),
        one=False
    )
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})


# 分页查询作业列表
@assignment_view.route('/list', methods=['GET'])
def list():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    course_id = request.args.get('course_id')
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql="select count(*) as total_count from assignment a inner join course c on a.course_id = c.id and c.state = 1 where a.course_id = %s and a.state = 1 and (a.assignment_name like %s or a.assignment_requirement like %s)",
        args=(course_id, search_query, search_query)
    )
    print(count)
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/assignment/list?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    res = db.query(
        sql="select a.id,a.assignment_name,a.assignment_requirement,DATE_FORMAT(a.submit_deadline_time, '%Y-%m-%d %H:%i') as submit_deadline_time,a.file_name,DATE_FORMAT(a.create_time, '%Y-%m-%d %H:%i:%S') as create_time from assignment a inner join course c on a.course_id = c.id and c.state = 1 where a.course_id = %s and a.state = 1 and (a.assignment_name like %s or a.assignment_requirement like %s) limit %s,%s",
        args=(course_id, search_query, search_query, offset, page_size),
        one=False)
    print(res)
    db.close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment_list': res, 'pages': pages}})


# 根据id查询作业详情
@assignment_view.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    assignment = DBHandler().query(
        sql="select id,assignment_name,assignment_requirement,DATE_FORMAT(submit_deadline_time, '%Y-%m-%d %H:%i') as submit_deadline_time,file_name from assignment where state = 1 and id = %s",
        args=(id,)
    )
    DBHandler().close()
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'assignment': assignment}})


# 添加作业
@assignment_view.route('/add', methods=['POST'])
def add():
    course_id = request.get_json().get('course_id')
    assignment_name = request.get_json().get('assignment_name')
    assignment_requirement = request.get_json().get('assignment_requirement')
    submit_deadline_time = request.get_json().get('submit_deadline_time')
    file_name = request.get_json().get('file_name')
    print('add--------', course_id, assignment_name, assignment_requirement, submit_deadline_time, file_name)
    if not course_id or not assignment_name or not assignment_requirement or not submit_deadline_time or not file_name:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='insert into assignment(course_id,assignment_name,assignment_requirement,submit_deadline_time,file_name) values(%s,%s,%s,%s,%s)',
        args=(course_id, assignment_name, assignment_requirement, submit_deadline_time, file_name)
    )
    assignment_id = db.get_insert_id()
    # 查询该课程下的学生
    students = db.query(
        sql="select student_id from student_course where course_id = %s and state = 1 and status = 1",
        args=(course_id,),
        one=False
    )
    if students and len(students) > 0:
        rows = [(assignment_id, stu['student_id']) for stu in students]
        db.exec(
            sql='insert into student_assignment(assignment_id,student_id) values(%s,%s)',
            args=rows,
            one=False
        )
    db.close()
    return jsonify({'code': 200, 'msg': '添加成功'})


# 修改作业
@assignment_view.route('/update', methods=['POST'])
def update():
    id = request.get_json().get('id')
    assignment_name = request.get_json().get('assignment_name')
    assignment_requirement = request.get_json().get('assignment_requirement')
    submit_deadline_time = request.get_json().get('submit_deadline_time')
    file_name = request.get_json().get('file_name')
    if not id or not assignment_name or not assignment_requirement or not submit_deadline_time or not file_name:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='update assignment set assignment_name = %s,assignment_requirement = %s,submit_deadline_time = %s,file_name = %s where state = 1 and id = %s',
        args=(assignment_name, assignment_requirement, submit_deadline_time, file_name, id)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '修改成功'})


# 删除作业
@assignment_view.route('/delete', methods=['POST'])
def delete():
    id = request.get_json().get('id')
    if not id:
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    db = DBHandler()
    db.exec(
        sql='update assignment set state = 0 where id = %s',
        args=(id,)
    )
    # 删除学生作业数据
    db.exec(
        sql='update student_assignment set state = 0 where assignment_id = %s',
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})
