import json

from ml.preprocessing_data.Articles_path import get_path
from ml.preprocessing_data.check_subject import check_sub


def marked_subject(sub_json, sub_orig):
    # sub_json название json файла предмета
    # sub_orig название предмета
    with open(get_path(sub_json), 'r') as file:
        data = json.load(file)
    sections_names = data['sections']
    pages_start = data['page_start']
    pages_end = data['page_end']
    files_name = data['path_to_pdf']
    obj = {
        "name": sub_orig,
        "themes": []
    }
    for i in range(len(sections_names)):
        cur_section = {
            'name': sections_names[i],
            'page_start': pages_start[i],
            'page_end': pages_end[i],
            'file_name': files_name[i]
        }
        obj['themes'].append(cur_section)
    return obj


def marked_list():
    obj = {
        'subjects': [

        ]
    }
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)
    for i in range(len(data['json_name'])):
        sub_json = data['json_name'][i]
        orig_json = data['orig_name'][i]
        marked_sub = marked_subject(sub_json, orig_json)
        obj['subjects'].append(marked_sub)
    return obj['subjects']
