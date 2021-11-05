from requests.exceptions import HTTPError
from requests.models import InvalidURL
from app.utils import cache_header
from flask.blueprints import Blueprint
from flask.helpers import make_response, url_for
from flask import render_template
import requests


blueprint = Blueprint(
    'cors_anywhere',
    __name__,
    url_prefix='/cors',
    template_folder='../templates',
    static_folder='../bundle',
)


@blueprint.route('/<path:url>')
@cache_header(max_age=3600)
def cors_anywhere(url: str):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        response = make_response(
            requests.get(url).text,
        )
    except:
        return render_template('500.html'), 500
    response.headers['Access-Control-Allow-Origin'] = url_for('main.index')
    return response
