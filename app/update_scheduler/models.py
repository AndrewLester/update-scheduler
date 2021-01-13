# type: ignore
from app.exts import db


class Update(db.Model):
    __tablename__ = 'update'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realm_name = db.Column(db.String, nullable=False)
    realm_id = db.Column(db.Integer, nullable=False)
    body = db.Column(db.String, nullable=False)
    attachments = db.Column(db.String, nullable=False)
    job = db.relationship(
        'ScheduledJob',
        uselist=False,
        backref=db.backref('update', cascade='all, delete-orphan', single_parent=True)
    )


class ScheduledJob(db.Model):
    __tablename__ = 'scheduled_job'

    id = db.Column(db.Integer, primary_key=True)
    # Both in UTC
    scheduled_at = db.Column(db.DateTime, nullable=False)
    scheduled_for = db.Column(db.DateTime, nullable=False)
    update_id = db.Column(db.Integer, db.ForeignKey('update.id', name='fk_update_id'), nullable=False)
