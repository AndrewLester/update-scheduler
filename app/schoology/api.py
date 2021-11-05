from app.schoology.types import Realm
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Any, Dict, List
from app.exts import cache, oauth_client as oauth
from app.main.models import User
import time

from app.utils import LocalizableTz

# Schoology prevents more than 15 requests in 5 seconds, or 1 request ever third of a second.
# This limit can be avoided safely by waiting for more than a third of a second before every request
MAX_SECONDS_PER_REQUEST = 0.34


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
        res = request_function(
            next_url if next_url else endpoint, *request_args, **request_kwargs)
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


@cache.memoize(timeout=300)
def get_user_realms(user: User) -> List[Realm]:
    sections: List[Realm] = [
        {'id': section['id'], 'name': section['course_title'],
            'type': 'sections'}
        for section in oauth.schoology.get(  # type: ignore
            f'users/{user.id}/sections'
        ).json()['section']
    ]
    groups: List[Realm] = [
        {'id': group['id'], 'name': group['title'], 'type': 'groups'}
        for group in oauth.schoology.get(  # type: ignore
            f'users/{user.id}/groups'
        ).json()['group']
    ]
    school: List[Realm] = (
        [{'id': user.building_id, 'name': 'School', 'type': 'schools'}]
        if user.building_id
        else []
    )
    district: List[Realm] = (
        [{'id': user.school_id, 'name': 'District', 'type': 'districts'}]
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

    return oauth.schoology.post(f'{realm}/updates', json=data)  # type: ignore


def post_updates(realms: List[Realm], body: str, attachments: List[Dict]):
    data: Dict[Any, Any] = {
        'body': body,
    }
    if attachments:
        data['attachments'] = attachments

    if isinstance(realms, str):
        return oauth.schoology.post(f'{realms}/updates', json=data)

    responses = []
    for realm in realms:
        response = oauth.schoology.post(  # type: ignore
            f'{realm["type"]}/{realm["id"]}/updates', json=data)
        responses.append(response)
        time.sleep(MAX_SECONDS_PER_REQUEST)
    return responses
