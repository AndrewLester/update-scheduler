# type: ignore
from typing import Dict
from app.exts import db


class Update(db.Model):
    __tablename__ = 'update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realm_type = db.Column(db.String(10), nullable=False)
    realm_id = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    attachments = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.String(30), db.ForeignKey('user.id', name='fk_user_id'), nullable=False)
    job = db.relationship(
        'ScheduledJob',
        uselist=False,
        backref=db.backref('update', single_parent=True),
        cascade='all, delete-orphan'
    )

    def post(self):
        pass

    def to_json(self):
        return {
            'id': self.id,
            'realm_type': self.realm_type,
            'realm_id': self.realm_id,
            'body': self.body,
            'attachments': self.attachments,
            'job': self.job.to_json() if self.job else None
        }

class ScheduledJob(db.Model):
    __tablename__ = 'scheduled_job'

    id = db.Column(db.String(35), primary_key=True)
    # Both in UTC
    scheduled_at = db.Column(db.DateTime, nullable=False)
    scheduled_in = db.Column(db.Interval)
    scheduled_for = db.Column(db.DateTime)
    update_id = db.Column(db.Integer, db.ForeignKey('update.id', name='fk_update_id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'scheduled_at': str(self.scheduled_at),
            'scheduled_in': str(self.scheduled_in) if self.scheduled_in else None,
            'scheduled_for': str(self.scheduled_for) if self.scheduled_for else None
        }
