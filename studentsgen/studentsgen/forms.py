from wtforms import Form, StringField, TextAreaField, validators
from wtforms import IntegerField, PasswordField
from wtforms.widgets import HiddenInput

strip_filter = lambda x: x.strip() if x else None

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=5)])

class AddWorkForm(Form):
    course = IntegerField('Course')
    title = StringField('Work name', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    max_point = IntegerField('Max Point')

class UpdateRatingForm(Form):
    student_id = IntegerField('Student')
    work=IntegerField('Work')
    point=IntegerField('Point')

