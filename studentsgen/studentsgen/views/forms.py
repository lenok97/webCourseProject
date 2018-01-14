from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
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
    AddNamedForm,
    AddStudentForm,
    AddCourseForm
)

@view_config(route_name='register', renderer='../templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data)
        new_user.set_role('base') #при регистрации доступ только для просмотра
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}


@view_config(route_name='update_rating', renderer='../templates/update_rating.jinja2')
def update_rating(request):
    user = request.user
    if user is None or (user.role != 'editor'):
        raise HTTPForbidden
    
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
    user = request.user
    if user is None or (user.role != 'editor'):
        raise HTTPForbidden
    
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

@view_config(route_name='add_student', renderer='../templates/add_student.jinja2', permission='create')
def add_student(request):
    form = AddStudentForm(request.POST)

    query = request.dbsession.query(Group)

    form.groups.choices = []
    for group in query:
        form.groups.choices.append((group.id, group.name))

    if request.method == 'POST' and form.validate():
        student = Student(name=form.name.data, group_id=request.params['groups'])
        request.dbsession.add(student)
        return HTTPFound(location=request.route_url('admin'))
    return { 'form' : form }

@view_config(route_name='add_course', renderer='../templates/add_course.jinja2', permission='create')
def add_course(request):
    form = AddCourseForm(request.POST)

    query = request.dbsession.query(Group)
    form.groups.choices = []
    for group in query:
        form.groups.choices.append((group.id, group.name))

    query = request.dbsession.query(Professor)
    form.professors.choices = []
    for professor in query:
        form.professors.choices.append((professor.id, professor.name))

    query = request.dbsession.query(Subject)
    form.subjects.choices = []
    for subject in query:
        form.subjects.choices.append((subject.id, subject.name))

    if request.method == 'POST' and form.validate():
        course = Course(group_id=request.params['groups'], professor_id=request.params['professors'], subject_id=request.params['subjects'])
        request.dbsession.add(course)
        return HTTPFound(location=request.route_url('admin'))
    return { 'form' : form }