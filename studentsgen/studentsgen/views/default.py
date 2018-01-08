from pyramid.response import Response
from pyramid.view import view_config

import sqlalchemy as sa
from sqlalchemy.exc import DBAPIError

from ..models import Student


@view_config(route_name='home', renderer='../templates/mainpage.jinja2')
def home_view(request):
    return {'one': 'one', 'project': 'StudentsGen'}

@view_config(route_name='student', renderer='../templates/student.jinja2')
def students_view(request):
	query = request.dbsession.query(Student)
	return { "students" : query.order_by(sa.desc(Student.name)) }

@view_config(route_name='admin', renderer='../templates/admin.jinja2')
def my_view2(request):
    return {}

@view_config(route_name='professor', renderer='../templates/professor.jinja2')
def my_view4(request):
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
