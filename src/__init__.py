from flask import Flask, render_template, session, redirect

app = Flask(__name__)
app.config.from_pyfile('../config.py')

from src.views.user import user_view
from src.views.notice import notice_view
from src.views.lecture import lecture_view
from src.views.file import file_view
from src.views.course import course_view
from src.views.assignment import assignment_view
from src.views.student_course import student_course_view
from src.views.message_board import message_board_view
from src.views.student_assignment import student_assignment_view
from src.views.message import message_view

app.register_blueprint(user_view)
app.register_blueprint(notice_view)
app.register_blueprint(lecture_view)
app.register_blueprint(file_view)
app.register_blueprint(course_view)
app.register_blueprint(assignment_view)
app.register_blueprint(student_course_view)
app.register_blueprint(message_board_view)
app.register_blueprint(student_assignment_view)
app.register_blueprint(message_view)


@app.route('/')
def index():
    if session.get('user'):
        return redirect('/user/' + session.get('user').get('role') + '/')
    else:
        return render_template('index.html')
