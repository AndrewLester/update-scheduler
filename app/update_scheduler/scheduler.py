from typing import Union
from app.update_scheduler.models import ScheduledJob, Update
from app.schoology.api import post_update
from app.exts import db, oauth_client as oauth
from datetime import datetime, timedelta
from rq import Queue
import pytz


def schedule_update(queue: Queue, dt: Union[datetime, timedelta], update: Update):
    """Schedule a schoology update for a certain time in the future"""
    if isinstance(dt, datetime):
        job = queue.enqueue_at(
            dt.astimezone(pytz.utc),
            post_update,
            update.realm_type + '/' + update.realm_id,
            update.body,
            update.attachments
        )
    else:
        job = queue.enqueue_in(
            dt,
            post_update,
            update.realm_type + '/' + update.realm_id,
            update.body,
            update.attachments
        )
    
    scheduled_job = ScheduledJob(
        id=job.id,
        scheduled_at=job.created_at,
        scheduled_in=dt if isinstance(dt, timedelta) else None,
        scheduled_for=dt if isinstance(dt, datetime) else None
    )
    update.job = scheduled_job
    db.session.add(update)  # type: ignore
    db.session.commit()  # type: ignore
    return job
