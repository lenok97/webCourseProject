from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError
from ..forms import RegistrationForm, AddWorkForm, UpdateRatingForm
from pyramid.security import remember, forget
from ..models import Student, Professor, Subject, Group, Course, Work, Rating, User

@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}

@view_config(route_name='updatereiting', renderer='../templates/updatereiting.jinja2', permission='create')
def updatereiting(request):
    form = UpdateRatingForm(request.POST)
    if request.method == 'POST' and form.validate():
        reiting = Rating(work_id=form.work.data)
        reiting.set_student(form.student_id.data)
        reiting.set_point(form.point.data) 
        request.dbsession.add(reiting)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}

@view_config(route_name='addwork', renderer='../templates/addwork.jinja2', permission='create')
def add_work(request):
    form = AddWorkForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_work = Work(name=form.title.data.encode('utf8'))
        new_work.set_maxpoint(form.max_point.data)
        request.dbsession.add(new_work)
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