# type: ignore
from flask_login import UserMixin
from sqlalchemy.orm import backref

from app.exts import db, login


@login.user_loader
def load_user(id):
    user = User.query.get(str(id))
    if user is not None and user.oauth_token is None:
        user = None
    return user


class User(UserMixin, db.Model):
    id: str = db.Column(db.String(36), primary_key=True)
    username: str = db.Column(db.String(64))
    email: str = db.Column(db.String(120))
    building_id: str = db.Column(db.String(36))
    school_id: str = db.Column(db.String(36))
    timezone: str = db.Column(db.String(120))
    profile_picture_url: str = db.Column(db.String(250))
    updates = db.relationship(
        'Update',
        backref='user'
    )
    oauth_token = db.relationship(
        'OAuth1Token',
        uselist=False,
        backref=backref('user', single_parent=True),
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
