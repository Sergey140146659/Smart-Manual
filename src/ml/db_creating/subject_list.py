import json

from ml.preprocessing_data.Articles_path import get_path


def get_subject_list():
    with open(get_path("subjects.json"), 'r') as file:
        data = json.load(file)
    return data['orig_name']


def get_subject_pdf(json_name):
    with open(get_path(json_name), 'r') as file:
        data = json.load(file)
    pdf = []
    for i in data['path_to_pdf']:
        if i not in pdf:
            pdf.append(i)
    return pdf


def get_files_list():
    with open(get_path("subjects.json"), 'r') as file:
        data = json.load(file)
    ans = {}
    for json_name, orig_name in zip(data['json_name'], data['orig_name']):
        ans[orig_name] = get_subject_pdf(json_name)
    return ans
