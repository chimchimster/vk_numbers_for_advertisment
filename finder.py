import json
import os
import re
import time
import requests
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

token = os.environ.get('vk_token')
COUNT = 1000


def get_people_ids(query, offset=0):

    script_exec_people_ids = f"""
        var people = API.users.search({{"q": "{query}", "fields": "has_mobile", "count": {COUNT}, "offset": {offset}}});
        return people.items@.id;
    """

    response = requests.post(f'https://api.vk.com/method/execute?code={script_exec_people_ids}&access_token={token}&v=5.131')

    return json.loads(response.text).get('response')


def get_full_data(people_ids):

    script_exec_full_data = f"""
        var data = API.users.get({{"user_ids": "{','.join(map(str, people_ids))}", "fields": "contacts"}});
        
        return [data@.id, data@.mobile_phone, data@.first_name, data@.last_name];
    """

    response_data = requests.post(f'https://api.vk.com/method/execute?code={script_exec_full_data}&access_token={token}&v=5.131')

    return json.loads(response_data.text).get('response')


def offset_checker(group_id):

    response = requests.post(f'https://api.vk.com/method/groups.getMembers?group_id={group_id}&access_token={token}&v=5.131')

    count = json.loads(response.text).get('response').get('count')

    return count


def get_groups():
    return 'laza_podsmotreno', 'lazarevskoe_love', 'lazarevskoe_podsl'


def get_members(group_id, offset, count=1000):
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


def data_handler(data):

    return [[data[0][i], data[1][i], data[2][i], data[3][i]] for i in range(len(data[0])) if data[1][i] and re.findall(r'(\+79|89)(\d{9})', data[1][i])]


def main():
    group_result = []
    groups = get_groups()

    for group in groups:
        offset = offset_checker(group)

        members_ids = get_members(group, offset)

        step = 1000
        for start in range(0, len(members_ids), step):
            full_data = get_full_data(members_ids[start:start+step])

            group_result.append(data_handler(full_data))

        df = pd.DataFrame(*group_result, columns=['vk_id', 'телефон', 'имя', 'фамилия'])
        df.to_excel('numbers.xlsx', sheet_name=f'{group}')


if __name__ == '__main__':
    main()
