from flask import current_app
from app.schoology.types import Realm
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, cast
from app.exts import cache, oauth_client as oauth
from app.main.models import User

from app.utils import LocalizableTz


def get_paged_data(
    request_function, 
    endpoint: str, 
    data_key: str,
    next_key: str = 'links',
    max_pages: int = -1, 
    *request_args, 
    **request_kwargs
):
    """Collect multiple pages of data from a paged REST API endpoint"""
    data = []
    page = 0
    next_url = ''
    while next_url is not None and (page < max_pages or max_pages == -1):
        res = request_function(next_url if next_url else endpoint, *request_args, **request_kwargs)
        try:
            json = res.json()
        except JSONDecodeError:
            return data
        
        next_url = json[next_key].get('next')
        data += json[data_key]
        page += 1

    return data


def schoology_to_datetime(string: str, tz: LocalizableTz) -> datetime:
    """Turn a Schoology time string into a datetime object with specified timezone"""
    time = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    # Turn naive time into local time at the specified timezone. Accounts for DST
    return tz.localize(time)


def datetime_to_schoology(time: datetime) -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S')


@cache.memoize(timeout=900)
def get_user_realms(user: User) -> List[Realm]:
    sections: List[Realm] = [
        {'id': section['id'], 'name': section['course_title'], 'realm_type': 'sections'}
        for section in oauth.schoology.get(
            f'users/{user.id}/sections'
        ).json()['section']
    ]
    groups: List[Realm] = [
        {'id': group['id'], 'name': group['title'], 'realm_type': 'groups'}
        for group in oauth.schoology.get(
            f'users/{user.id}/groups'
        ).json()['group']
    ]
    school: List[Realm] = (
        [{'id': user.building_id, 'name': 'School', 'realm_type': 'schools'}]
        if user.building_id
        else []
    )
    district: List[Realm] = (
        [{'id': user.school_id, 'name': 'District', 'realm_type': 'districts'}]
        if user.school_id and user.school_id != user.building_id
        else []
    )

    return sections + groups + school + district


def post_update(realm: str, body: str, attachments: List[Dict]):
    data: Dict[Any, Any] = {
        'body': body,
    }
    if attachments:
        data['attachments'] = attachments

    return oauth.schoology.post(f'{realm}/updates', json=data)
