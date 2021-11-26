# type: ignore
from app.schoology.api import datetime_to_schoology
from typing import Dict
from app.exts import db
import isodate
from datetime import datetime


update_realm = db.Table('update_realm', db.Model.metadata,
                        db.Column('update_id', db.ForeignKey(
                            'update.id'), primary_key=True),
                        db.Column('realm_id', db.ForeignKey(
                            'realm.id'), primary_key=True)
                        )


class Update(db.Model):
    __tablename__ = 'update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey(
        'user.id', name='fk_user_id'), nullable=False)
    realms = db.relationship(
        'Realm',
        secondary=update_realm
    )
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
            'body': self.body,
            'attachments': [attachment.to_json() for attachment in self.attachments],
            'realms': [realm.to_json() for realm in self.realms],
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
    summary = db.Column(db.Text)
    image = db.Column(db.Text)
    icon = db.Column(db.Text)
    update_id = db.Column(db.Integer, db.ForeignKey(
        'update.id', name='fk_attachment_update_id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'image': self.image,
            'icon': self.icon,
            'url': self.url,
            'summary': self.summary
        }

    def to_schoology_json(self):
        return {
            'type': self.type,
            'title': self.title,
            'url': self.url,
            'summary': self.summary,
            'thumbnail': self.image or self.icon
        }


class Realm(db.Model):
    __tablename__ = 'realm'

    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(150))

    def to_json(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name
        }
