from secrets import token_urlsafe

from authlib.common.errors import AuthlibBaseError
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
from werkzeug.routing import BuildError

from app import db, oauth_client as oauth
from app.main.models import User

from .models import OAuth1Token

from app.schoology.domain import authorization_domain

blueprint = Blueprint(
    'oauth',
    __name__,
    url_prefix='/oauth',
    template_folder='../..templates',
    static_folder='../../static',
)


@blueprint.route('/logout')
@login_required
def logout():
    """
    Logs you out of Calendar Mixer. You will have to log in again to access your Calendar.
    Your Calendar Mixer feed will continue to update even if you are logged out.
    """
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('main.index'))


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        flash('You\'re already logged in.')
        return redirect(url_for('main.index'))

    requested_url = request.args.get('next') or ''
    domain = authorization_domain(request.args.get('domain'))

    next_query_arg = f'?next={requested_url}' if requested_url else ''
    redirect_uri = url_for('.authorize', _external=True) + next_query_arg

    oauth.schoology.authorize_url = domain
    return oauth.schoology.authorize_redirect(redirect_uri, oauth_callback=redirect_uri)


@blueprint.route('/authorize')
def authorize():
    try:
        token = oauth.schoology.authorize_access_token()
    except (AuthlibBaseError):
        flash('Please restart the login procedure...')
        return render_template('500.html'), 500

    user_data = oauth.schoology.get('users/me').json()

    user = User.query.filter_by(username=user_data['username']).first()
    if user is None:
        user = User(
            id=user_data['uid'],
            username=user_data['username'],
            email=user_data['primary_email'],
            timezone=user_data['tz_name'],
            building_id=str(user_data['building_id']),
            school_id=str(user_data['school_id']),
            profile_picture_url=user_data['picture_url']
        )

    oauth_token = OAuth1Token(
        name='schoology',
        oauth_token=token['oauth_token'],
        oauth_token_secret=token['oauth_token_secret'],
    )
    user.oauth_token = oauth_token

    db.session.add(user)  # type: ignore
    db.session.commit()  # type: ignore

    login_user(user, remember=True)
    next_url = request.args.get('next') or url_for('main.index')
    return redirect(next_url)
