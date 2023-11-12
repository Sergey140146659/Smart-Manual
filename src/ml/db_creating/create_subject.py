import json
import re

from PyPDF2 import PdfReader

from ml.db_creating.pdf_reader import get_text
from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text
from src.ml.preprocessing_data.check_subject import check_sub, create_sub_name


def create_subject(obj):
    # name
    # themes
    # path
    if check_sub(obj['name']) != 0:
        with open(obj['path'], 'r') as file:
            data = json.load(file)
        index = check_sub(obj['name'])
        json_name = data['json_name'][index]
        with open(get_path(json_name), 'r') as file:
            subject_info = json.load(file)
        for info in obj['themes']:
            theme, pages = info["theme_name"], info["pages"]
            subject_info['sections'].append(theme)
            subject_info['pages_number_of_sections'].append(pages)
            text = get_text(['path'], pages) + ' ' + theme
            subject_info['text_of_sections'].append(text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append(obj['path'])
        with open(get_path(json_name), "w") as file:
            json.dump(subject_info, file)
    else:
        json_name = create_sub_name()
        with open(get_path('subjects.json'), 'r') as file:
            data = json.load(file)
        data['json_name'].append(json_name)
        data['orig_name'].append(obj['name'])
        data['questions'].append([])
        data['lemma_questions'].append([])
        with open(get_path('subjects.json'), "w") as file:
            json.dump(data, file)

        sub_info = {
            "sections": [],
            "pages_number_of_sections": [],
            "text_of_sections": [],
            "lemma_text_of_sections": [],
            "combined_text_of_sections": [],
            "path_to_pdf": []
        }
        with open(get_path(json_name), "w") as file:
            json.dump(sub_info, file)

        with open(get_path(json_name), 'r') as file:
            subject_info = json.load(file)
        for info in obj['themes']:
            theme, pages = info["theme_name"], info["pages"]
            subject_info['sections'].append(theme)
            subject_info['pages_number_of_sections'].append(pages)
            text = get_text(obj['path'], pages) + ' ' + theme
            subject_info['text_of_sections'].append(text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append(obj['path'])

        with open(get_path(json_name), "w") as file:
            json.dump(subject_info, file)
