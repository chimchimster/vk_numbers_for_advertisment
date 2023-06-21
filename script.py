import os
import re
import time
import json
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
token = os.environ.get('vk_token')

offset = 0
for i in range(100):

    script_exec_members_ids = f"""
        var people = API.groups.getMembers({{"group_id": "gorodf", "fields": "has_mobile", "count": 1000, "offset": {offset}}});

        var people_ids =  people.items@.id;

        return people_ids;
    """

    response_ids = requests.post(f'https://api.vk.com/method/execute?code={script_exec_members_ids}&access_token={token}&v=5.131')
    time.sleep(1)
    offset += 1000

    script_exec_full_data = f"""
        var result = [];
        var data = API.users.get({{"user_ids": "{','.join(map(str, json.loads(response_ids.text).get('response')))}", "fields": "contacts,bdate,sex"}});
        result += [data@.mobile_phone, data@.first_name, data@.last_name, data@.bdate, data@.sex];
        return result;
    """

    response_data = requests.post(f'https://api.vk.com/method/execute?code={script_exec_full_data}&access_token={token}&v=5.131')

    data = json.loads(response_data.text).get('response')

    try:
        list_of_results = [(data[0][x], data[1][x], data[2][x]) for x in range(len(data[0])) if data[0][x] and re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', data[0][x]) and 536457600 <= datetime.strptime('-'.join([data[3][0].split('.')[2], data[3][0].split('.')[1], data[3][0].split('.')[0]]), "%Y-%m-%d").timestamp() <= 1104516061 and data[4][x] == 2]
    except:
        list_of_results = []

    with open('phone_numbers.txt', 'a') as file:
        for tpl in list_of_results:
            file.write(','.join(tpl) + '\n')
