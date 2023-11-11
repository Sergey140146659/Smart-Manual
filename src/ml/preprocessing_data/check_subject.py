import json
import os


def check_sub(sub):
    if not os.path.isfile('subjects.json'):
        return
    with open('subjects.json', 'r') as file:
        data = json.load(file)
    for key,val in data.items():
        if key == sub:
            return True
    return False

def create_sub_name():
    with open('subjects.json', 'r') as file:
        data = json.load(file)
    json_name = data['subjects']
    num = 1
    while True:
        name = 'subject' + str(num)
        if name in json_name:
            continue
        else: