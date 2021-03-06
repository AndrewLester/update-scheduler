from app.utils import IntervalField
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.core import DateTimeField, FieldList, FormField, IntegerField
from wtforms.validators import NoneOf, Required, Regexp, URL


class Attachment(FlaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, meta={'csrf': False})

    id = IntegerField()
    type = StringField(validators=[Regexp('(file|link|video)')])
    title = StringField()
    url = StringField(validators=[URL()])
    image = StringField()
    icon = StringField()
    summary = StringField()


class ScheduledJob(FlaskForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs, meta={'csrf': False})

    id = StringField()
    scheduled_for = DateTimeField()
    scheduled_in = IntervalField()


class UpdateForm(FlaskForm):
    id = IntegerField(validators=[Required()])
    realm_type = StringField('Update course type', validators=[Required(), Regexp('(courses|groups|schools|districts|sections)')])
    realm_id = StringField('Update course ID', validators=[Required()])
    body = StringField('Update body', validators=[Required(), NoneOf('<p><br></p>')])

    job = FormField(ScheduledJob, label='Post time')
    attachments = FieldList(FormField(Attachment, label='Attachment'))
