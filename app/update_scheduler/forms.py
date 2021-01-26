from app.utils import IntervalField
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.core import DateTimeField, FormField
from wtforms.validators import Length, Required, Regexp


class ScheduledJob(FlaskForm):
    scheduled_for = DateTimeField()
    scheduled_in = IntervalField()


class UpdateForm(FlaskForm):
    id = StringField(validators=[Required()])
    realm_type = StringField(validators=[Required(), Regexp('(course|group|school|district)')])
    realm_id = StringField(validators=[Required(), Length(5)])
    body = StringField(validators=[Required()])
    attachments = StringField(default='')

    job = FormField(ScheduledJob)
