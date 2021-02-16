from typing import Union, cast
from app.update_scheduler.models import ScheduledJob, Update
from app.exts import db
from datetime import datetime, timedelta
from rq import Queue
import pytz


POST_UPDATE_TASK = 'app.tasks.post_update_task'


def schedule_update(queue: Queue, dt: Union[datetime, timedelta], update: Update):
    """Schedule a schoology update for a certain time in the future"""
    if isinstance(dt, datetime):
        job = queue.enqueue_at(
            dt.astimezone(pytz.utc),
            POST_UPDATE_TASK,
            update.realm_type + '/' + update.realm_id,
            update.body,
            update.attachments
        )
    else:
        job = queue.enqueue_in(
            dt,
            POST_UPDATE_TASK,
            update.realm_type + '/' + update.realm_id,
            update.body,
            update.attachments
        )
    user_timezone = pytz.timezone(update.user.timezone)
    scheduled_at = pytz.utc.localize(cast(datetime, job.created_at or datetime.utcnow())).astimezone(user_timezone)

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
