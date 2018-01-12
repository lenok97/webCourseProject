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

    query = request.dbsession.query(Group)
    group = query.get(student.group_id)

    query = request.dbsession.query(Course)
    sub_query = request.dbsession.query(Subject)

    courses = []
    subjects = []
    for course in query.filter(Course.group_id == group.id):
        courses.append(course)
        subjects.append(sub_query.get(course.subject_id))

    data = zip(courses, subjects)

    return { 'student' : student, 'group' : group, 'data' : data }

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
    for rating in query.filter(Rating.student_id == student.id ):
        work = work_query.get(rating.work_id)

        if work.course_id == course.id:
            ratings.append(rating)
            works.append(work_query.get(rating.work_id))

    data = zip(ratings, works)

    return { 'subject' : subject, 'professor' : professor, 'data' : data }