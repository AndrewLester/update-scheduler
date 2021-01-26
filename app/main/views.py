from flask import Blueprint, flash, render_template, abort
from flask_login.utils import login_required

from app.exts import oauth_client as oauth

blueprint = Blueprint(
    'main',
    __name__, 
    template_folder='../templates', 
    static_folder='../static'
)


@blueprint.route('/')
def index():
    return render_template('index.html')


@blueprint.route('/tutorial')
def tutorial():
    return render_template('tutorial.html', title='Tutorial')


@blueprint.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')


@blueprint.route('/login')
def login():
    return render_template('login.html', title='Login')


@blueprint.route('/profile')
@login_required
def profile():
    """
    Displays basic Schoology info for the current user signed into Calendar Mixer.
    Not a replacement for Schoology's profile viewer, as this one is incomplete.
    """
    resp = oauth.schoology.get('users/me', cache=True)
    if resp.status_code >= 400:
        flash('Schoology API error...')
        abort(500)
    return render_template('user.html', profile=resp.json())


@blueprint.route('/googleef1db03e70a6de9a.html')
def google_site_verif():
    return render_template('googleef1db03e70a6de9a.html')
