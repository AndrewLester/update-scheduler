# type: ignore
from app.schoology.api import datetime_to_schoology
from typing import Dict
from app.exts import db
import isodate
from datetime import datetime


class Update(db.Model):
    __tablename__ = 'update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realm_type = db.Column(db.String(10), nullable=False)
    realm_id = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey(
        'user.id', name='fk_user_id'), nullable=False)
    job = db.relationship(
        'ScheduledJob',
        uselist=False,
        backref=db.backref('update', single_parent=True),
        cascade='all, delete-orphan'
    )
    attachments = db.relationship(
        'Attachment',
        backref=db.backref('update'),
        cascade='all, delete-orphan'
    )

    def to_json(self):
        return {
            'id': self.id,
            'realm_type': self.realm_type,
            'realm_id': self.realm_id,
            'body': self.body,
            'attachments': [attachment.to_json() for attachment in self.attachments],
            'job': self.job.to_json() if self.job else None
        }


class ScheduledJob(db.Model):
    __tablename__ = 'scheduled_job'

    id = db.Column(db.String(36), primary_key=True)
    # Both in UTC
    scheduled_at: datetime = db.Column(db.DateTime, nullable=False)
    scheduled_in = db.Column(db.Interval)
    scheduled_for = db.Column(db.DateTime)
    update_id = db.Column(db.Integer, db.ForeignKey(
        'update.id', name='fk_update_id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'scheduled_at': datetime_to_schoology(self.scheduled_at),
            'scheduled_in': isodate.duration_isoformat(self.scheduled_in) if self.scheduled_in else None,
            'scheduled_for': datetime_to_schoology(self.scheduled_for) if self.scheduled_for else None
        }


class Attachment(db.Model):
    __tablename__ = 'attachment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(5), nullable=False)
    title = db.Column(db.String(200))
    url = db.Column(db.String(300), nullable=False)
    thumbnail = db.Column(db.Text)
    update_id = db.Column(db.Integer, db.ForeignKey(
        'update.id', name='fk_attachment_update_id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'url': self.url
        }
    
    def to_schoology_json(self):
        return {
            'type': self.type,
            'title': self.title,
            'url': self.url
        }
