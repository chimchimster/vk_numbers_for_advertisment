import os
import time
import json
import requests

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

        response = requests.post(f'https://api.vk.com/method/execute?code={script_exec_members_ids}&access_token={token}&v=5.131')

        time.sleep(1)

        members_ids = json.loads(response.text).get('response')

        group_result += members_ids

    return group_result


def get_full_data(members_ids: list) -> list:
    """ Function which retrieves full data about members. """

    script_exec_full_data = f"""
        var data = API.users.get({{"user_ids": "{','.join(map(str, members_ids))}", "fields": "contacts,sex"}});

        return [data@.first_name, data@.last_name, data@.mobile_phone, data@.sex];
    """

    response_data = requests.post(f'https://api.vk.com/method/execute?code={script_exec_full_data}&access_token={token}&v=5.131')

    return json.loads(response_data.text).get('response')


def offset_checker(group_id: str) -> int:
    """ Check if there is a pagination. """

    response = requests.post(f'https://api.vk.com/method/groups.getMembers?group_id={group_id}&access_token={token}&v=5.131')

    count = json.loads(response.text).get('response').get('count')

    return count


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