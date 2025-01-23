from flask import session, redirect, render_template
from functools import wraps
from src import app


# 404错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


# 判断登录用户是否是管理员
def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            if session.get('user').get('role') == 'admin':
                return func(*args, **kwargs)
            else:
                return render_template('403.html')
        else:
            return redirect('/user/login')

    return wrapper


# 判断登录用户是否是讲师
def is_instructor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            if session.get('user').get('role') == 'instructor':
                return func(*args, **kwargs)
            else:
                return render_template('403.html')
        else:
            return redirect('/user/login')

    return wrapper


# 判断登录用户是否是学生
def is_student(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            if session.get('user').get('role') == 'student':
                return func(*args, **kwargs)
            else:
                return render_template('403.html')
        else:
            return redirect('/user/login')

    return wrapper
