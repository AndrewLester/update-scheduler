from datetime import datetime, timedelta
from flask.globals import current_app
from flask_login.utils import login_required
from isodate.duration import Duration
import pytz
from rq.job import Job
from rq.exceptions import NoSuchJobError
from app.update_scheduler.scheduler import schedule_update
from typing import NoReturn, Optional, Union
from app.update_scheduler.forms import UpdateForm
from app.utils import rest_endpoint
from app.exts import db

from flask.templating import render_template
from app.update_scheduler.models import ScheduledJob, Update
from app.schoology.api import get_user_realms
from flask import jsonify, abort
from flask_login import current_user
from flask.blueprints import Blueprint


blueprint = Blueprint(
    'update_scheduler',
    __name__,
    url_prefix='/scheduler',
    template_folder='../templates',
    static_folder='../bundle',
)


@blueprint.route('')
@login_required
def scheduler():
    return render_template('scheduler.html')


@blueprint.route('/realms')
@login_required
def realms():
    realms = get_user_realms(current_user)  # type: ignore
    return jsonify(realms)


@rest_endpoint(
    blueprint=blueprint,
    route='/updates',
    model=Update,
    form=UpdateForm,
    methods={'GET', 'POST', 'PUT', 'DELETE'}
)
@login_required
def updates(form: UpdateForm) -> Union[Update, NoReturn]:
    update = Update.query.get(form.id.data)
    if update is None:
        update = Update(
            realm_type=form.realm_type.data,
            realm_id=form.realm_id.data,
            body=form.body.data,
            attachments=form.attachments.data,
            user_id=current_user.id
        )

        if form.job.scheduled_for.data or form.job.scheduled_in.data:
            schedule_update(
                current_app.redis_queue,
                scheduled_formdata_to_time(
                    form.job.scheduled_for.data,
                    form.job.scheduled_in.data
                ),
                update
            )
    else:
        update.realm_type = form.realm_type.data
        update.realm_id = form.realm_id.data
        update.body = form.body.data
        update.attachments = form.attachments.data

        if update.job is not None:
            try:
                job = Job.fetch(update.job.id, connection=current_app.redis)
            except NoSuchJobError:
                db.session.delete(update.job)
            else:
                job.cancel()

        if form.job.scheduled_for.data or form.job.scheduled_in.data:
            schedule_update(
                current_app.redis_queue,
                scheduled_formdata_to_time(
                    form.job.scheduled_for.data,
                    form.job.scheduled_in.data
                ),
                update
            )
        else:
            update.job = None

    return update


def scheduled_formdata_to_time(
    scheduled_for: Optional[datetime],
    scheduled_in: Optional[Union[timedelta, Duration]]
) -> Union[datetime, timedelta]:
    """
    Aborts if neither option has a value. Only put this in view functions
    when a return value is necessary.
    """
    if scheduled_for is not None:
        return pytz.timezone(current_user.timezone).localize(scheduled_for)
    elif scheduled_in is not None:
        return scheduled_in.tdelta if isinstance(scheduled_in, Duration) else scheduled_in
    abort(400)