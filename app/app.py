from logging import Logger
from typing import Optional

import dill
from rq import Queue
import redis
from flask import Flask, render_template, jsonify, flash, g
from flask.cli import load_dotenv
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from app import login, db, migrate, cache, csrf, oauth_client
from app import update_scheduler, main, oauth, cors_anywhere
from config import Config


def create_app(config=Config):
    load_dotenv()
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app.redis = redis.from_url(app.config['REDIS_URL'])
    app.redis_queue = Queue(
        name=app.config['APP_NAME'].lower().replace(' ', '-'),
        serializer=dill,  # type: ignore
        connection=app.redis
    )

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    app.shell_context_processor(lambda: {
        'db': db, 'User': main.models.User, 'Update': update_scheduler.models.Update,
        'OAuth1Token': oauth.models.OAuth1Token,
        'ScheduledJob': update_scheduler.models.ScheduledJob,
        'Attachment': update_scheduler.models.Attachment
    })

    return app


def register_extensions(app: Flask):
    login.init_app(app)
    login.login_view = 'main.login'  # type: ignore
    db.init_app(app)
    cache.init_app(app, config=app.config)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':  # type: ignore
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    def fetch_token(name: str) -> Optional[dict]:
        user_id = getattr(current_user, 'id', False) or g.user_id
        item = oauth.models.OAuth1Token.query.filter_by(
            name=name, user_id=user_id
        ).first()

        return item.to_token()

    oauth_client.init_app(app, fetch_token=fetch_token, cache=cache)
    oauth_client.register(
        name='schoology',
        api_base_url='https://api.schoology.com/v1/',
        request_token_url='https://api.schoology.com/v1/oauth/request_token',
        access_token_url='https://api.schoology.com/v1/oauth/access_token',
        authorize_url='https://www.schoology.com/oauth/authorize',
        client_id=app.config['SCHOOLOGY_CLIENT_ID'],
        client_secret=app.config['SCHOOLOGY_CLIENT_SECRET']
    )
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main.views.blueprint)
    app.register_blueprint(oauth.views.blueprint)
    app.register_blueprint(update_scheduler.views.blueprint)
    app.register_blueprint(cors_anywhere.views.blueprint)


def register_errorhandlers(app):
    app.register_error_handler(404, lambda _: (
        render_template('404.html'), 404))
    app.register_error_handler(CSRFError, lambda error: (
        jsonify(errors=[error.description]), 400))

    def internal_error(error):
        db.session.rollback()  # type: ignore
        flash('Internal Error: Try refreshing')
        return render_template('500.html'), 500

    app.register_error_handler(500, internal_error)
