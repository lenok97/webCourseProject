from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from ..forms import RegistrationForm, AddWorkForm, UpdateRatingForm
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

    query = request.dbsession.query(Course)
    sub_query = request.dbsession.query(Subject)
    group_query = request.dbsession.query(Group)

    courses = []
    groups = []
    for course in query.filter(Course.professor_id == professor.id):
        courses.append(sub_query.get(course.subject_id))
        groups.append(group_query.get(course.group_id))

    data = zip(courses, groups)

    return { 'professor' : professor, 'data' : data }