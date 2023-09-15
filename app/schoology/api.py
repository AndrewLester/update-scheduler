from app.schoology.types import Realm
from datetime import datetime
from json.decoder import JSONDecodeError
from typing import Any, Dict, List, Optional, cast
from app.exts import cache, oauth_client as oauth
from app.main.models import User
import time
from collections import Counter

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


@cache.memoize(timeout=21600)
def get_user_schools(
    school_id: Optional[str],
    building_id: Optional[str],
    additional_buildings: Optional[str]
) -> List[Realm]:
    building_id = building_id or school_id
    schools: List[Realm] = []
    buildings_response: Optional[Dict[str, List[Dict]]] = None

    if school_id:
        school = oauth.schoology.get(  # type: ignore
            f'schools/{school_id}').json()
        schools.append({
            'id': school['id'],
            'name': school['title'],
            'type': 'schools'
        })

        buildings_response = oauth.schoology.get(  # type: ignore
            f'schools/{school_id}/buildings'
        )

        if buildings_response.ok and buildings_response.text:  # type: ignore
            buildings_response = buildings_response.json()  # type: ignore
        else:
            buildings_response = None

    if buildings_response:
        realms: List[Realm] = [
            {'id': str(school['id']), 'name': school['title'],
             'type': 'schools'}
            for school in buildings_response['building']
        ]
        schools += realms

    if building_id and all([school['id'] != building_id for school in schools]):
        school = oauth.schoology.get(  # type: ignore
            f'schools/{building_id}').json()
        schools.append({
            'id': school['id'],
            'name': school['title'],
            'type': 'schools'
        })

    if additional_buildings:
        building_ids = additional_buildings.split(',')
        building_ids = [b_id for b_id in building_ids if all(
            [school['id'] != b_id for school in schools])]
        for building_id in building_ids:
            school = oauth.schoology.get(  # type: ignore
                f'schools/{building_id}').json()

            schools.append({
                'id': school['id'],
                'name': school['title'],
                'type': 'schools'
            })

    return schools


def get_user_sections(user: User) -> List[Realm]:
    sections_response = oauth.schoology.get(  # type: ignore
        f'users/{user.id}/sections'
    )

    if not sections_response.ok:
        return []

    sections = [
        {'id': section['id'], 'name': section['course_title'], 'section_name': section.get('section_title', ''),
            'type': 'sections'}
        for section in sections_response.json()['section']
    ]

    section_name_counts = Counter([section['name'] for section in sections])
    for section in sections:
        if section_name_counts[section['name']] > 1:
            section['name'] += f": {section['section_name']}"
        del section['section_name']

    return cast(List[Realm], sections)


def get_user_groups(user: User) -> List[Realm]:
    groups_response = oauth.schoology.get(  # type: ignore
        f'users/{user.id}/groups'
    )

    if not groups_response.ok:
        return []

    return [
        {'id': group['id'], 'name': group['title'], 'type': 'groups'}
        for group in groups_response.json()['group']
    ]


@cache.memoize(timeout=300)
def get_user_realms(user: User) -> List[Realm]:
    user_data = oauth.schoology.get('users/me').json()  # type: ignore

    sections = get_user_sections(user)
    groups = get_user_groups(user)

    school_id = str(user_data.get('school_id', ''))
    building_id = str(user_data.get('building_id', ''))
    additional_buildings = str(user_data.get('additional_buildings', ''))

    schools = get_user_schools(school_id, building_id, additional_buildings)

    return sections + groups + schools


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
        return oauth.schoology.post(  # type: ignore
            f'{realms}/updates', json=data
        )

    responses = []
    for realm in realms:
        response = oauth.schoology.post(  # type: ignore
            f'{realm["type"]}/{realm["id"]}/updates', json=data)
        responses.append(response)
        time.sleep(MAX_SECONDS_PER_REQUEST)
    return responses
