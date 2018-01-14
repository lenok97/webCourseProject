from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from pyramid.security import remember, forget
from ..models import Student, Professor, Subject, Group, Course, Work, Rating, User

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

@view_config(route_name='professor_course', renderer='../templates/professor_course.jinja2')
def professor_course_view(request):
    course_id = request.matchdict['c']
    query = request.dbsession.query(Course)
    course = query.get(course_id)

    return { 'course' : course }