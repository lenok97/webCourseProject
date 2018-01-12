from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from ..forms import RegistrationForm, AddWorkForm, UpdateStudentRatingForm
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
    subjects = []
    groups = []
    for course in query.filter(Course.professor_id == professor.id):
        courses.append(course)
        subjects.append(sub_query.get(course.subject_id))
        groups.append(group_query.get(course.group_id))

    data = zip(courses, subjects, groups)

    return { 'professor' : professor, 'data' : data }

@view_config(route_name='professor_course', renderer='../templates/professor_course.jinja2')
def professor_course_view(request):
    professor_id = request.matchdict['p']
    course_id = request.matchdict['c']

    query = request.dbsession.query(Professor)
    professor = query.get(professor_id)

    query = request.dbsession.query(Course)
    course = query.get(course_id)

    query = request.dbsession.query(Subject)
    subject = query.get(course.subject_id)

    query = request.dbsession.query(Group)
    group = query.get(course.group_id)

    query = request.dbsession.query(Work)
    work_query = request.dbsession.query(Work)

    works = []
    for work in query.filter(Work.course_id == course.id):
        works.append(work)

    return { 'professor' : professor, 'course' : course, 'subject' : subject, 'group' : group, 'works' : works }