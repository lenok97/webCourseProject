from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from wtforms import IntegerField
from pyramid.security import remember, forget
from ..models import Student, Professor, Subject, Group, Course, Work, Rating, User
from ..forms import (
    RegistrationForm,
    AddWorkForm,
    UpdateGroupRatingForm,
    UpdateStudentRatingForm,
    AddNamedForm
)

@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}

@view_config(route_name='auth', match_param='action=in', renderer='string',
             request_method='POST')
@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)

@view_config(route_name='update_rating', renderer='../templates/update_rating.jinja2', permission='create')
def update_rating(request):
    professor_id = request.matchdict['p']
    course_id = request.matchdict['c']
    work_id = request.matchdict['w']

    query = request.dbsession.query(Work)
    work = query.get(work_id)

    query = request.dbsession.query(Course)
    course = query.get(work.course_id)

    query = request.dbsession.query(Student)
    students = query.filter(Student.group_id == course.group_id).order_by(sa.desc(Student.name))

    form = UpdateGroupRatingForm(request.POST)

    n = 0
    for student in students:
        form.students.append_entry()
        form.students[n].point.label = student.name
        form.students[n].point.data = 0
        n += 1

    if request.method == 'POST' and form.validate():
        query = request.dbsession.query(Rating)

        n = 0
        for student in students:
            point = request.params[form.students[n].point.id]

            rating = query.filter(Rating.work_id == work.id, Rating.student_id == student.id).one_or_none()

            if rating == None:
                rating = Rating(work_id=work.id, student_id=student.id, point=point)
                request.dbsession.add(rating)
            else:
                rating.point = point
            n += 1
        return HTTPFound(location=request.route_url('professor_course', p=professor_id, c=course_id))

    return { 'form': form, 'students' : students, 'professor_id' : professor_id, 'course_id' : course_id, 'work' : work }

@view_config(route_name='add_work', renderer='../templates/addwork.jinja2', permission='create')
def add_work(request):
    professor_id = request.matchdict['p']
    course_id = request.matchdict['c']

    form = AddWorkForm(request.POST)

    if request.method == 'POST' and form.validate():
        work = Work(course_id=course_id, name=form.title.data, max_point=form.max_point.data)
        request.dbsession.add(work)
        return HTTPFound(location=request.route_url('professor_course', p=professor_id, c=course_id))

    return { 'form': form, 'professor_id' : professor_id, 'course_id' : course_id }

@view_config(route_name='add_professor', renderer='../templates/add_professor.jinja2', permission='create')
def add_professor(request):
    form = AddNamedForm(request.POST)
    if request.method == 'POST' and form.validate():
        professor = Professor(name=form.name.data)
        request.dbsession.add(professor)
        return HTTPFound(location=request.route_url('admin'))
    return { 'form' : form }

@view_config(route_name='add_group', renderer='../templates/add_group.jinja2', permission='create')
def add_professor(request):
    form = AddNamedForm(request.POST)
    if request.method == 'POST' and form.validate():
        group = Group(name=form.name.data)
        request.dbsession.add(group)
        return HTTPFound(location=request.route_url('admin'))
    return { 'form' : form }

@view_config(route_name='add_subject', renderer='../templates/add_subject.jinja2', permission='create')
def add_subject(request):
    form = AddNamedForm(request.POST)
    if request.method == 'POST' and form.validate():
        subject = Subject(name=form.name.data)
        request.dbsession.add(subject)
        return HTTPFound(location=request.route_url('admin'))
    return { 'form' : form }