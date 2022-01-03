from typing import Union, cast
from app.update_scheduler.models import ScheduledJob, Update
from app.exts import db
from datetime import datetime, timedelta
from rq import Queue
from app.main.models import User
import pytz


POST_UPDATE_TASK = 'app.tasks.post_update_task'


def schedule_update(queue: Queue, dt: Union[datetime, timedelta], update: Update):
    """Schedule a schoology update for a certain time in the future"""
    attachments = [attachment.to_schoology_json()
                   for attachment in update.attachments]
    realms = [realm.to_json() for realm in update.realms]
    if isinstance(dt, datetime):
        job = queue.enqueue_at(
            dt.astimezone(pytz.utc),
            POST_UPDATE_TASK,
            realms,
            '',  # TODO: Remove this and the string param to the task once all tasks using the old system are sent
            attachments
        )
    else:
        job = queue.enqueue_in(
            dt,
            POST_UPDATE_TASK,
            realms,
            '',  # TODO: Remove this and the string param to the task once all tasks using the old system are sent
            attachments
        )
    user_timezone = pytz.timezone(User.query.get(update.user_id).timezone)
    scheduled_at = pytz.utc.localize(
        cast(datetime, job.created_at or datetime.utcnow())).astimezone(user_timezone)

    scheduled_job = ScheduledJob(
        id=job.id,
        scheduled_at=scheduled_at,
        scheduled_in=dt if isinstance(dt, timedelta) else None,
        scheduled_for=dt if isinstance(dt, datetime) else None
    )
    update.job = scheduled_job
    db.session.add(update)  # type: ignore
    db.session.commit()  # type: ignore
    return job
