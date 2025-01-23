from flask import Blueprint, request, render_template, redirect, session, jsonify
from src.util.db import DBHandler
from src.util.common import Page
from hashlib import md5
from src.util.interceptor import is_admin, is_instructor, is_student

user_view = Blueprint('user', __name__, url_prefix='/user')


# 登录
@user_view.route('/login', methods=['GET', 'POST'])
def login():
    # 如果是get访问，就显示登录页面
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if username == '' or password == '' or role == '':
            return render_template('login.html', error='用户名、密码和角色不能为空')
        # 去数据库校验用户名和密码是否正确
        password = md5(password.encode()).hexdigest()
        user = DBHandler().query(sql='select * from user where username=%s and password=%s and role=%s and state=1',
                                args=(username, password, role))
        DBHandler().close()
        if user:
            if user['status'] == 1:
                # 登录成功
                session['user'] = user
                return redirect('/user/' + role + '/')
            else:
                return render_template('login.html', error='该用户已被禁用')
        else:
            return render_template('login.html', error='用户名或密码错误')


# 退出登录
@user_view.route('/logout', methods=['GET'])
def logout():
    # 删除指定的key的session
    session.pop('user')
    return redirect('/user/login')


# 修改密码
@user_view.route('/change-password', methods=['POST'])
def change_password():
    old_password = request.get_json().get('old_password')
    new_password = request.get_json().get('new_password')
    confirm_password = request.get_json().get('confirm_password')
    if old_password == '' or new_password == '' or confirm_password == '':
        return jsonify({'code': 400, 'msg': '参数不能为空'})
    # 去数据库校验用户名和密码是否正确
    old_password = md5(old_password.encode()).hexdigest()
    user = DBHandler().query(sql='select * from user where username=%s and password=%s and state = 1',
                            args=(session.get('user').get('username'), old_password))
    DBHandler().close()
    if user:
        if user['status'] == 1:
            # 登录成功
            if new_password == confirm_password:
                new_password = md5(new_password.encode()).hexdigest()
                DBHandler().exec(sql='update user set password=%s where username=%s',
                                 args=(new_password, session.get('user').get('username')))
                DBHandler().close()
                return jsonify({'code': 200, 'msg': '修改成功'})
            else:
                return jsonify({'code': 400, 'msg': '两次输入的密码不一致'})
        else:
            return jsonify({'code': 400, 'msg': '该用户已被禁用'})
    else:
        return jsonify({'code': 400, 'msg': '旧密码输入错误'})


# 管理员相关
# 管理员首页
@user_view.route('/admin/', methods=['GET'])
@is_admin
def admin_index():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('admin/index.html', username=username, numberId=number_id)


# 学生管理
@user_view.route('/admin/student-manage', methods=['GET'])
@is_admin
def admin_student_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('admin/student_manage.html', username=username, numberId=number_id)


# 教师管理
@user_view.route('/admin/instructor-manage', methods=['GET'])
@is_admin
def admin_instructor_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('admin/instructor_manage.html', username=username, numberId=number_id)


# 讲座管理
@user_view.route('/admin/lecture-manage', methods=['GET'])
@is_admin
def admin_lecture_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('admin/lecture_manage.html', username=username, numberId=number_id)


# 通知管理
@user_view.route('/admin/notice-manage', methods=['GET'])
@is_admin
def admin_notice_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('admin/notice_manage.html', username=username, numberId=number_id)


# 查询全部正常用户
@user_view.route('/all', methods=['GET'])
def all():
    users = DBHandler().query(sql='SELECT id,username from user where state = 1 and `status` = 1', one=False)
    DBHandler().close()
    print(users)
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'users': users}})


# 根据角色查询用户列表
@user_view.route('/role-all', methods=['GET'])
def role_all():
    role = request.args.get('role')
    users = DBHandler().query(sql='SELECT id,username from user where state = 1 and `status` = 1 and role = %s',
                             args=(role,),
                             one=False)
    DBHandler().close()
    print(users)
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'users': users}})


# 根据角色查询用户分页列表
@user_view.route('/role', methods=['GET'])
@is_admin
def role():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 2))
    role = request.args.get('role')
    search = request.args.get('search', '')
    search_query = '%' + search + '%'
    db = DBHandler()
    count = db.query(
        sql='SELECT count(*) as total_count from user where state = 1 and role = %s and username like %s',
        args=(role, search_query)
    )
    page_params = {
        'total_count': count['total_count'],
        'page_size': page_size,
        'page': page,
        'url': '/user/role?page='
    }
    pages = Page(page_params)
    # 取分页数据
    offset = (page - 1) * page_size
    users = db.query(
        sql='SELECT id,username,number_id,DATE_FORMAT(create_time, "%Y-%m-%d %H:%i:%S") AS create_time,status from user where state = 1 and role = %s and username like %s limit %s,%s',
        args=(role, search_query, offset, page_size),
        one=False
    )
    db.close()
    print(users)
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'user_list': users, 'pages': pages}})


# 根据id查询单个用户
@user_view.route('/get', methods=['GET'])
def get():
    id = request.args.get('id')
    user = DBHandler().query(
        sql='SELECT id,username,number_id,role,DATE_FORMAT(create_time, "%Y-%m-%d %H:%i:%S") AS create_time,status from user where state = 1 and id = %s',
        args=(id,))
    DBHandler().close()
    print(user)
    return jsonify({'code': 200, 'msg': '查询成功', 'data': {'user': user}})


# 添加用户
@user_view.route('/add', methods=['POST'])
@is_admin
def add():
    username = request.get_json().get('username')
    password = md5('123456'.encode()).hexdigest()
    role = request.get_json().get('role')
    number_id = request.get_json().get('number_id')
    status = request.get_json().get('status')
    if username == '' or role == '' or number_id == '':
        return jsonify({'code': 400, 'msg': '用户名、角色和学号不能为空'})
    db = DBHandler()
    # 去数据库校验用户是否已存在
    user = db.query(sql='select * from user where state = 1 and username=%s and role=%s and number_id=%s',
                   args=(username, role, number_id))
    if user:
        return jsonify({'code': 400, 'msg': '该用户已存在'})
    # 添加用户
    db.exec(
        sql='insert into user(username,password,number_id,role, status) values(%s,%s,%s,%s,%s)',
        args=(username, password, number_id, role, status)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '添加成功'})


# 修改用户
@user_view.route('/update', methods=['POST'])
@is_admin
def update():
    id = request.get_json().get('id')
    username = request.get_json().get('username')
    role = request.get_json().get('role')
    number_id = request.get_json().get('number_id')
    status = request.get_json().get('status')
    if id == '' or username == '' or role == '' or number_id == '':
        return jsonify({'code': 400, 'msg': '用户名、角色和学号不能为空'})
    DBHandler().exec(
        sql='update user set username = %s,role = %s, number_id = %s, `status` = %s where id = %s',
        args=(username, role, number_id, status, id)
    )
    DBHandler().close()
    return jsonify({'code': 200, 'msg': '修改成功'})


# 删除用户
@user_view.route('/delete', methods=['POST'])
@is_admin
def delete():
    id = request.get_json().get('id')
    if id == '':
        return jsonify({'code': 400, 'msg': '用户id不能为空'})
    db = DBHandler()
    user = db.query(
        sql='SELECT id,status from user where state = 1 and id = %s',
        args=(id,))
    # 判断用户状态
    if (user['status'] == 1):
        return jsonify({'code': 400, 'msg': '正常用户无法删除'})
    db.exec(
        sql='update user set state = 0 where id = %s',
        args=(id,)
    )
    db.close()
    return jsonify({'code': 200, 'msg': '删除成功'})


# 讲师相关
# 讲师首页
@user_view.route('/instructor/', methods=['GET'])
@is_instructor
def instructor_index():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('instructor/index.html', username=username, numberId=number_id)


# 课程作业管理
@user_view.route('/instructor/assignment-manage', methods=['GET'])
@is_instructor
def instructor_assignment_manage():
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('instructor/assignment_manage.html', username=username, numberId=number_id,
                           course_id=course_id, course_name=course_name)


# 通知管理
@user_view.route('/instructor/notice-manage', methods=['GET'])
@is_instructor
def instructor_notice_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('instructor/notice_manage.html', username=username, numberId=number_id)


# 讲座管理
@user_view.route('/instructor/lecture-manage', methods=['GET'])
@is_instructor
def lecture_notice_manage():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('instructor/lecture_manage.html', username=username, numberId=number_id)


# 教师联系学生页面
@user_view.route('/instructor/contact-student', methods=['GET'])
@is_instructor
def instructor_contact_student():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    student_id = request.args.get('stu_id')
    student_name = request.args.get('stu_name')
    course_name = request.args.get('course_name')
    return render_template('instructor/contact_student.html', username=username, numberId=number_id,
                           contact_user_id=student_id, contact_user_name=student_name, course_name=course_name)


# 学生相关
# 学生首页
@user_view.route('/student/', methods=['GET'])
@is_student
def student_index():
    user_id = session.get('user').get('id')
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('student/index.html', user_id=user_id, username=username, numberId=number_id)


# 学生课程详情页
@user_view.route('/student/course', methods=['GET'])
@is_student
def student_course():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    instructor_id = request.args.get('instructor_id')
    instructor_name = request.args.get('instructor_name')
    return render_template('student/course.html', username=username, numberId=number_id, course_id=course_id,
                           course_name=course_name, instructor_id=instructor_id, instructor_name=instructor_name)


# 学生课程作业列表页
@user_view.route('/student/assignment-list', methods=['GET'])
@is_student
def student_assignment_list():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    return render_template('student/assignment_list.html', username=username, numberId=number_id, course_id=course_id,
                           course_name=course_name)


# 学生课程作业查看结果页
@user_view.route('/student/assignment-result', methods=['GET'])
@is_student
def student_assignment_result():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    return render_template('student/assignment_result.html', username=username, numberId=number_id, course_id=course_id,
                           course_name=course_name)


# 学生选课页面
@user_view.route('/student/course-request', methods=['GET'])
@is_student
def student_course_request():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    return render_template('student/course_request.html', username=username, numberId=number_id)


# 学生联系课程讲师页面
@user_view.route('/student/contact-instructor', methods=['GET'])
@is_student
def student_contact_instructor():
    username = session.get('user').get('username')
    number_id = session.get('user').get('number_id')
    instructor_id = request.args.get('instructor_id')
    instructor_name = request.args.get('instructor_name')
    course_name = request.args.get('course_name')
    return render_template('student/contact_instructor.html', username=username, numberId=number_id,
                           contact_user_id=instructor_id, contact_user_name=instructor_name, course_name=course_name)
