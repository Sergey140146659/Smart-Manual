import json

from ml.preprocessing_data.Articles_path import get_path


def get_subject_list():
    with open(get_path("subjects.json"), 'r') as file:
        data = json.load(file)
    return data['orig_name']

