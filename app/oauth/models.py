# type: ignore
from typing import Dict
from app.exts import db


class OAuth1Token(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    oauth_token = db.Column(db.String(48), nullable=False)
    oauth_token_secret = db.Column(db.String(48))
    user_id = db.Column(db.String(36),
                        db.ForeignKey('user.id', name='fk_user_id'),
                        unique=True,
                        nullable=False)

    def to_token(self) -> Dict[str, str]:
        return {
            'oauth_token': self.oauth_token,
            'oauth_token_secret': self.oauth_token_secret,
        }
