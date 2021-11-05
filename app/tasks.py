from rq.job import Job
from app.schoology.types import Realm
from app.update_scheduler.models import ScheduledJob
from typing import Dict, List

from flask import g
from app.exts import db
from app.schoology.api import post_updates
from app.app import create_app
from rq import get_current_job

app = create_app()
app.app_context().push()


def post_update_task(realms: List[Realm], body: str, attachments: List[Dict]):
    job: Job = get_current_job()  # type: ignore

    with app.app_context():
        scheduled_job = ScheduledJob.query.get(job.id)
        if scheduled_job is None:
            app.logger.error(
                f'Scheduled job with id {job.id} could not be found when trying to post')
            return

        update = scheduled_job.update
        g.user_id = update.user_id
        responses = post_updates(realms, body, attachments)
        if type(responses) is list:
            app.logger.info('Posted updates with response codes: ' +
                            ', '.join([str(response.status_code) for response in responses]))

        job.cleanup(0)
        db.session.delete(update)  # type: ignore
        db.session.commit()  # type: ignore
        job.delete()
        g.user_id = -1
