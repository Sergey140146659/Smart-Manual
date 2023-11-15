import json
import os

from ml.preprocessing_data.Articles_path import get_path


def check_sub(sub):
    if not os.path.isfile(get_path('subjects.json')):
        return 0
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)
        for i in range(len(data['orig_name'])):
            if data['orig_name'][i] == sub:
                return i
        return False



def create_sub_name():
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)
<<<<<<< Updated upstream
    return 'subject' + str(len(data['orig_name']) + 1) + '.json'
=======
    return 'subject' + str(len(data['orig_name']) + 1) + '.json'

>>>>>>> Stashed changes
