from app.utils import FlaskSubform, IntervalField
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.core import DateTimeField, FieldList, FormField, IntegerField
from wtforms.validators import Length, NoneOf, Required, Regexp, URL


class Attachment(FlaskSubform):
    id = IntegerField()
    type = StringField(validators=[Regexp('(file|link|video)')])
    title = StringField()
    url = StringField(validators=[URL(), Length(max=300)])
    image = StringField()
    icon = StringField()
    summary = StringField()


class Realm(FlaskSubform):
    id = StringField()
    type = StringField(
        validators=[Regexp('(courses|groups|schools|districts|sections)')])
    name = StringField()


class ScheduledJob(FlaskSubform):
    id = StringField()
    scheduled_for = DateTimeField()
    scheduled_in = IntervalField()


class UpdateForm(FlaskForm):
    id = IntegerField(validators=[Required()])
    body = StringField('Update body', validators=[
                       Required(), NoneOf('<p><br></p>')])

    job = FormField(ScheduledJob, label='Post time')
    attachments = FieldList(FormField(Attachment, label='Attachment'))
    realms = FieldList(FormField(Realm, label="Realm"), min_entries=1)
