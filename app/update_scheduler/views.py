from app.update_scheduler.forms import UpdateForm
from app.utils import rest_endpoint

from flask.templating import render_template
from app.update_scheduler.models import Update
from app.schoology.api import get_user_realms
from flask import jsonify
from flask_login import current_user
from flask.blueprints import Blueprint


blueprint = Blueprint(
    'update_scheduler',
    __name__,
    url_prefix='/scheduler',
    template_folder='../templates',
    static_folder='../bundle',
)


@blueprint.route('/')
def scheduler():
    return render_template('scheduler.html')    


@blueprint.route('/realms')
def realms():
    realms = get_user_realms(current_user)
    return jsonify(realms)


@rest_endpoint(
    blueprint=blueprint,
    route='/updates',
    model=Update,
    form=UpdateForm,
    methods={'GET', 'POST', 'PUT', 'DELETE'}
)
def updates():
    pass