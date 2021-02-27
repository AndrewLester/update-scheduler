from app.update_scheduler.models import ScheduledJob
from typing import Dict, List

from flask import g, current_app
import traceback
from app.exts import db
from app.schoology.api import post_update
from app.app import create_app
from rq import get_current_job

app = create_app()
app.app_context().push()


def post_update_task(realm: str, body: str, attachments: List[Dict]):
    job = get_current_job()

    with app.app_context():
        scheduled_job = ScheduledJob.query.get(job.id)
        if scheduled_job is None:
            app.logger.error(f'Scheduled job with id {job.id} could not be found when trying to post')
            return

        update = scheduled_job.update
        g.user_id = update.user_id

        res = post_update(realm, body, attachments)
        app.logger.info('Posted update with response code: ' + str(res.status_code))

        job.cleanup(0)
        db.session.delete(update)  # type: ignore
        db.session.commit()  # type: ignore
        job.delete()
        g.user_id = -1
