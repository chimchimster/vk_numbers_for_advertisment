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











def get_groups():
    return 'laza_podsmotreno', 'lazarevskoe_love', 'lazarevskoe_podsl'


def data_handler(data):

    return [(data[0][i], ''.join(re.findall(r'(\+79|89)(\d{9})', data[1][i])[0]), data[2][i], data[3][i]) for i in range(len(data[0])) if data[1][i] and re.findall(r'(\+79|89)(\d{9})', data[1][i])]


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

    result = []
    for lst in group_result:
        for item in lst:
            result.append(item)

    df = pd.DataFrame(result, columns=['vk_id', 'телефон', 'имя', 'фамилия'])
    df.to_excel('numbers.xlsx', sheet_name=f'numbers')


if __name__ == '__main__':
    main()
# check
