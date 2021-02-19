import functools
from datetime import timedelta, datetime
from typing import (
    Any,
    Callable,
    Literal,
    NoReturn,
    Optional,
    Protocol,
    Set,
    Type,
    TypeVar,
    Union,
)

from flask import (
    abort,
    Response,
    request,
    make_response,
    request
)
from flask.blueprints import Blueprint
from flask.json import jsonify
from flask_login import current_user
from flask_login.utils import login_required
from flask_wtf.form import FlaskForm

from wtforms import Form
from wtforms.fields.core import Field
from wtforms.widgets.core import TextInput

import isodate

from app.exts import cache, db


HTTPMethod = Union[Literal['POST'], Literal['GET'],
                   Literal['PUT'], Literal['DELETE']]
Validator = Callable[[FlaskForm, Field], None]


class LocalizableTz(Protocol):
    def localize(self, dt: datetime, is_dst: bool = False) -> datetime:
        ...


class IntervalField(Field):
    widget = TextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = isodate.parse_duration(valuelist[0])
        else:
            self.data = None


def cache_header(max_age, **ckwargs):
    def decorator(view):
        f = cache.cached(max_age, **ckwargs)(view)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # Coerce view-function output to a response
            response: Response = make_response(f(*args, **kwargs))
            response.cache_control.max_age = max_age
            extra = timedelta(seconds=max_age)
            if response.last_modified is None:
                response.last_modified = datetime.utcnow()
            response.expires = response.last_modified + extra
            response.add_etag()
            return response.make_conditional(request)

        return wrapper

    return decorator


FormType = TypeVar('FormType', bound=Form)
ModelType = TypeVar('ModelType', bound=db.Model)  # type: ignore


def rest_endpoint(
    blueprint: Blueprint,
    route: str,
    model: Type[ModelType],  # type: ignore
    form: Type[FormType],  # type: ignore
    methods: Set[HTTPMethod],
) -> Callable:
    def decorator(func: Callable[[FormType], Union[ModelType, NoReturn]]) -> Callable[[int], Any]:
        @login_required
        @functools.wraps(func)
        def wrapper(id: Optional[int] = None):
            if request.method == 'GET' and 'GET' in methods:
                if id is not None:
                    model_instance = model.query.get_or_404(id)  # type: ignore
                    return jsonify(**model_instance.to_json())
                else:
                    return jsonify(
                        [
                            instance.to_json()
                            for instance in model.query.filter_by(  # type: ignore
                                user_id=current_user.id
                            ).all()
                        ]
                    )

            if request.method == 'DELETE' and 'DELETE' in methods and id is not None:
                model_instance = model.query.get_or_404(id)  # type: ignore
                db.session.delete(model_instance)  # type: ignore
                db.session.commit()  # type: ignore
                return jsonify(), 204

            form_data = form.from_json(request.get_json())  # type: ignore
            if not form_data.validate_on_submit():
                abort(make_response(jsonify(errors=form_data.errors), 400))

            if request.method == 'POST' and 'POST' in methods:
                model_instance = func(form_data)
                db.session.add(model_instance)  # type: ignore
                db.session.commit()  # type: ignore
                return model_instance.to_json()  # type: ignore

            if request.method == 'PUT' and 'PUT' in methods and id is not None:
                model_instance = func(form_data)
                db.session.add(model_instance)  # type: ignore
                db.session.commit()  # type: ignore
                return jsonify(), 200

            # Every possible correct option was exhausted
            return abort(400)

        # Route for non-identifying REST requests
        blueprint.add_url_rule(
            route,
            view_func=wrapper,
            methods=[method for method in methods if method in {
                'GET', 'POST'}],
        )
        # Route for identifying REST requests
        blueprint.add_url_rule(
            route + '/<int:id>',
            view_func=wrapper,
            methods=[method for method in methods if method in {
                'PUT', 'DELETE', 'GET'}],
        )

        return wrapper

    return decorator
