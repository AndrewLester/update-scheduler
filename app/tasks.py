from app.update_scheduler.models import ScheduledJob
from typing import Dict, List

from flask import g
from app.schoology.api import post_update
from app.app import create_app
from rq import get_current_job

app = create_app()
app.app_context().push()


def post_update_task(realm: str, body: str, attachments: List[Dict]):
    job = get_current_job()

    with app.app_context():
        g.user_id = ScheduledJob.query.get(job.id).update.user_id

        try:
            post_update(realm, body, attachments)
        except:
            pass
        finally:
            job.cleanup(0)