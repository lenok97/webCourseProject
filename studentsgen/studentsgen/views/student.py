from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from pyramid.security import remember, forget
from ..models import Student, Professor, Subject, Group, Course, Work, Rating, User

@view_config(route_name='students', renderer='../templates/students.jinja2')
def students_view(request):
    query = request.dbsession.query(Student)
    return { 'students' : query.order_by(sa.desc(Student.name)) }

@view_config(route_name='student', renderer='../templates/student.jinja2')
def student_view(request):
    student_id = request.matchdict['s']
    query = request.dbsession.query(Student)
    student = query.get(student_id)

    return { 'student' : student }

@view_config(route_name='student_course', renderer='../templates/student_course.jinja2')
def student_course_view(request):
    student_id = request.matchdict['s']
    course_id = request.matchdict['c']
    query = request.dbsession.query(Course)
    course = query.get(course_id)

    ratings = []
    works = []
    for rating, work in request.dbsession.query(Rating, Work).\
                                filter(Rating.student_id == student_id).\
                                filter(Rating.work_id == Work.id).\
                                filter(Work.course_id == course.id).\
                                all():
        ratings.append(rating)
        works.append(work)

    data = zip(ratings, works)

    return { 'course' : course, 'data' : data }