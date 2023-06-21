import os
import re
import time
import json
from dotenv import load_dotenv
import requests
import pandas as pd


load_dotenv()
token = os.environ.get('vk_token')
list_of_results = []
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
        result += [data@.first_name, data@.last_name, data@.mobile_phone, data@.bdate, data@.sex];
        return result;
    """

    response_data = requests.post(f'https://api.vk.com/method/execute?code={script_exec_full_data}&access_token={token}&v=5.131')

    data = json.loads(response_data.text).get('response')

    for i in range(len(data[0])):
        if data[2][i] and re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', data[2][i]) and re.findall(r'(\+77|87)(\d{9})', data[2][i]):
            format_number = list(re.findall(r'(\+77|87)(\d{9})', data[2][i])[0])

            format_number[0] = '+77'
            list_of_results.append((data[0][i] if data[0][i] else '', data[1][i] if data[1][i] else '', ''.join(format_number), data[3][i] if data[3][i] and len(data[3][i]) >= 8 else 'год рождения отсутствует', "мужчина" if data[4][i] == 2 else "женщина"))

    list_of_results = list(filter(lambda x: "777777" not in x[2] and "000000" not in x[2], list_of_results))


df = pd.DataFrame(list_of_results, columns=["Имя", "Фамилия", "Номер телефона", "Год рождения", "Пол"])
df.to_excel('phone_numbers.xlsx', sheet_name='phones')
