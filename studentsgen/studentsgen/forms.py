from wtforms import Form, StringField, TextAreaField, FieldList, FormField, validators
from wtforms import IntegerField, PasswordField
from wtforms.widgets import HiddenInput

strip_filter = lambda x: x.strip() if x else None

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=255)],
                           filters=[strip_filter])
    password = PasswordField('Password', [validators.Length(min=5)])

class AddWorkForm(Form):
    title = StringField('Work name', [validators.Length(min=1, max=255)],
                        filters=[strip_filter])
    max_point = IntegerField('Max Point')

class UpdateStudentRatingForm(Form):
    point=IntegerField('Point')

class UpdateGroupRatingForm(Form):
    students = FieldList(FormField(UpdateStudentRatingForm))

class AddNamedForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=255)], filters=[strip_filter])