# type: ignore
from typing import Dict
from app.exts import db


class Update(db.Model):
    __tablename__ = 'update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realm_type = db.Column(db.String, nullable=False)
    realm_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String, nullable=False)
    attachments = db.Column(db.String, nullable=False)
    job = db.relationship(
        'ScheduledJob',
        uselist=False,
        backref=db.backref('update', cascade='all, delete-orphan', single_parent=True)
    )

    def to_json(self):
        return {
            'id': self.id,
            'realm_type': self.realm_type,
            'realm_id': self.realm_id,
            'body': self.body,
            'attachments': self.attachments,
            'job': self.job.to_json()
        }

class ScheduledJob(db.Model):
    __tablename__ = 'scheduled_job'

    id = db.Column(db.String(), primary_key=True)
    # Both in UTC
    scheduled_at = db.Column(db.DateTime, nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    update_id = db.Column(db.Integer, db.ForeignKey('update.id', name='fk_update_id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'scheduled_at': self.scheduled_at,
            'scheduled_for': self.scheduled_for
        }
