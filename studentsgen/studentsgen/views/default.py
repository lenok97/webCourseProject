from pyramid.response import Response
from pyramid.view import view_config

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from ..models import Student, Professor, Subject, Group, Course, Work, Rating


@view_config(route_name='home', renderer='../templates/mainpage.jinja2')
def home_view(request):
    return {'one': 'one', 'project': 'StudentsGen'}

@view_config(route_name='students', renderer='../templates/students.jinja2')
def students_view(request):
    query = request.dbsession.query(Student)
    return { 'students' : query.order_by(sa.desc(Student.name)) }

@view_config(route_name='student', renderer='../templates/student.jinja2')
def student_view(request):
    student_id = request.matchdict['s']
    
    query = request.dbsession.query(Student)
    student = query.get(student_id)

    query = request.dbsession.query(Group)
    group = query.get(student.group_id)

    query = request.dbsession.query(Course)
    sub_query = request.dbsession.query(Subject)

    courses = []
    for course in query.filter(Course.group_id == group.id):
        courses.append(sub_query.get(course.subject_id))

    return { 'student' : student, 'group' : group, 'courses' : courses }

@view_config(route_name='student_course', renderer='../templates/student_course.jinja2')
def student_course_view(request):
    student_id = request.matchdict['s']
    course_id = request.matchdict['c']

    query = request.dbsession.query(Student)
    student = query.get(student_id)

    query = request.dbsession.query(Course)
    course = query.get(course_id)

    query = request.dbsession.query(Subject)
    subject = query.get(course.subject_id)

    query = request.dbsession.query(Professor)
    professor = query.get(course.professor_id)

    query = request.dbsession.query(Rating)
    work_query = request.dbsession.query(Work)

    ratings = []
    works = []
    for rating in query.filter(Rating.student_id == student.id):
        ratings.append(rating)
        works.append(work_query.get(rating.work_id))

    data = zip(ratings, works)

    return { 'subject' : subject, 'professor' : professor, 'data' : data }

@view_config(route_name='professors', renderer='../templates/professors.jinja2')
def professors_view(request):
    query = request.dbsession.query(Professor)
    return { 'professors' : query.order_by(sa.desc(Professor.name)) }

@view_config(route_name='professor', renderer='../templates/professor.jinja2')
def professor_view(request):
    professor_id = request.matchdict['p']

    query = request.dbsession.query(Professor)
    professor = query.get(professor_id)

    return { 'professor' : professor }

@view_config(route_name='admin', renderer='../templates/admin.jinja2')
def my_view2(request):
    return {}



db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_studentsgen_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
