import json
import re

from PyPDF2 import PdfReader

from ml.db_creating.pdf_reader import get_text
from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text
from ml.preprocessing_data.check_subject import check_sub, create_sub_name


def create_subject(obj):
    if check_sub(obj['name']) is not None:
        with open(get_path("subjects.json"), 'r') as file:
            data = json.load(file)
        index = check_sub(obj['name'])
        json_name = data['json_name'][index]
        with open(get_path(json_name), 'r') as file:
            subject_info = json.load(file)
        for info in obj['themes']:
            theme, page_start, page_end = info["theme_name"], info["page_start"], info["page_end"]
            subject_info['sections'].append(theme)
            subject_info["page_start"].append(page_start)
            subject_info["page_end"].append(page_end)
            text = get_text(obj['path'], page_start, page_end) + ' ' + theme
            subject_info['text_of_sections'].append(text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append(obj['path'])
            subject_info['questions'].append([])
            subject_info['lemma_questions'].append([])
        with open(get_path(json_name), "w") as file:
            json.dump(subject_info, file)
    else:
        json_name = create_sub_name()
        with open(get_path('subjects.json'), 'r') as file:
            data = json.load(file)
        data['json_name'].append(json_name)
        data['orig_name'].append(obj['name'])

        with open(get_path('subjects.json'), "w") as file:
            json.dump(data, file)

        sub_info = {
            "sections": [],
            "page_start": [],
            "page_end": [],
            "text_of_sections": [],
            "lemma_text_of_sections": [],
            "combined_text_of_sections": [],
            "path_to_pdf": [],
            "questions": [],
            "lemma_questions": []
        }
        with open(get_path(json_name), "w") as file:
            json.dump(sub_info, file)

        with open(get_path(json_name), 'r') as file:
            subject_info = json.load(file)
        for info in obj['themes']:
            theme, page_start, page_end = info["theme_name"], info["page_start"], info["page_end"]
            subject_info['sections'].append(theme)
            subject_info["page_start"].append(page_start)
            subject_info["page_end"].append(page_end)
            text = get_text(obj['path'], page_start, page_end) + ' ' + theme
            subject_info['text_of_sections'].append(text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append(obj['path'])
            subject_info['questions'].append([])
            subject_info['lemma_questions'].append([])
        with open(get_path(json_name), "w") as file:
            json.dump(subject_info, file)
