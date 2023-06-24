import os
import time
import json
import requests


from vk_numbers_for_advertisment.exceptions.exceptions import VKAPIException
from vk_numbers_for_advertisment.telegram_logs.telegram_logs import catch_log

token = os.environ.get('vk_token')


def get_members_ids(group_id: str, offset: int, count: int = 1000) -> list:
    """ Function which retrieves members ids from particular group. """

    group_result = []

    for step in range(0, offset, count):

        script_exec_members_ids = f"""
                var people = API.groups.getMembers({{"group_id": "{group_id}", "fields": "has_mobile", "count": {count}, "offset": {step}}});

                var people_ids =  people.items@.id;

                return people_ids;
            """

        try:
            response = requests.post(f'https://api.vk.com/method/execute?code={script_exec_members_ids}&access_token={token}&v=5.131')

            time.sleep(1)

            response_json = json.loads(response.text)

            check_errors(response_json)

            members_ids = response_json.get('response')

            group_result += members_ids

        except VKAPIException as v:
            catch_log(str(v), level='ERROR')

    return group_result


def get_full_data(members_ids: list) -> list:
    """ Function which retrieves full data about members. """

    script_exec_full_data = f"""
        var data = API.users.get({{"user_ids": "{','.join(map(str, members_ids))}", "fields": "contacts,sex,bdate,country,city"}});

        return data;
    """

    try:
        response_data = requests.post(f'https://api.vk.com/method/execute?code={script_exec_full_data}&access_token={token}&v=5.131')

        response_json = json.loads(response_data.text)

        check_errors(response_json)

        result = response_json.get('response')

        if result:
            return result

    except VKAPIException as v:
        catch_log(str(v), level='ERROR')

    return []


def offset_checker(group_id: str) -> int:
    """ Check if there is a pagination. """

    try:
        response = requests.post(f'https://api.vk.com/method/groups.getMembers?group_id={group_id}&access_token={token}&v=5.131')

        response_json = json.loads(response.text)

        check_errors(response_json)

        result = response_json.get('response')
        if result:
            return result.get('count')

    except VKAPIException as v:
        catch_log(str(v), level='ERROR')
    return 0


def check_errors(response_json):
    if response_json.get('error'):
        error_code = response_json['error']['error_code']
        log = str(VKAPIException(error_code))
        catch_log(log, level='ERROR')



# This func can be useful in future
# def get_people_ids(query, offset=0):
#
#     script_exec_people_ids = f"""
#         var people = API.users.search({{"q": "{query}", "fields": "has_mobile", "count": {COUNT}, "offset": {offset}}});
#         return people.items@.id;
#     """
#
#     response = requests.post(f'https://api.vk.com/method/execute?code={script_exec_people_ids}&access_token={token}&v=5.131')
#
#     return json.loads(response.text).get('response')