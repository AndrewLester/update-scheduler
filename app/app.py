# from app.blueprints.calendar import models

import functools
from typing import Optional
import pytz
import redis
# from authlib.client.client import OAuthClient
from flask import Flask, render_template, request, jsonify, g, send_from_directory, flash, current_app
from flask.cli import load_dotenv
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from flask_sitemap import sitemap_page_needed
# from requests_cache.backends.redis import RedisCache

from app import login, db, migrate, cache, csrf
# from app.blueprints import calendar, main, oauth
# from app.exts import oauth as oauth_client
from config import Config


def create_app(config=Config):
    load_dotenv()
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app.redis = redis.from_url(app.config['REDIS_URL'])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    app.shell_context_processor(lambda: {
        'db': db, #'User': main.models.User
    })

    return app


def register_extensions(app: Flask):
    login.init_app(app)
    login.login_view = 'main.login'  #type: ignore
    db.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)
    csrf.init_app(app)
    cache.init_app(app, config=app.config)

    def fetch_token(name) -> Optional[dict]:
        # item = oauth.models.OAuth1Token.query.filter_by(
        #     name=name, user_id=getattr(current_user, 'id', False)
        # ).first()
        # if item:
        #     return item.to_token()
        pass

    # oauth_client.init_app(app, fetch_token=fetch_token, cache=cache)
    # oauth_client.register(
    #     name='schoology',
    #     api_base_url='https://api.schoology.com/v1/',
    #     request_token_url='https://api.schoology.com/v1/oauth/request_token',
    #     access_token_url='https://api.schoology.com/v1/oauth/access_token',
    #     authorize_url='https://www.schoology.com/oauth/authorize',
    #     client_id=app.config['SCHOOLOGY_CLIENT_ID'],
    #     client_key=app.config['SCHOOLOGY_CLIENT_SECRET']
    # )


def register_blueprints(app):
    # app.register_blueprint(main.views.blueprint)
    # app.register_blueprint(update_scheduler.views.blueprint)
    pass


def register_errorhandlers(app):
    app.register_error_handler(404, lambda _: (render_template('404.html'), 404))
    app.register_error_handler(CSRFError, lambda error: (jsonify({'reason': error.description}), 400))

    def internal_error(error):
        db.session.rollback()  # type: ignore
        flash('Internal Error: Try refreshing')
        return render_template('500.html'), 500

    app.register_error_handler(500, internal_error)


def load_page(fn):
    @functools.wraps(fn)
    def loader(*args, **kwargs):
        page = kwargs.get('page')
        data = cache.get(str(page))
        return data if data else fn(*args, **kwargs)
    return loader
