import json
import re

from PyPDF2 import PdfReader

from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text
from src.ml.preprocessing_data.check_subject import check_sub, create_sub_name

str_to_replace = "!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–qwertyiopasdfghjklzxcvbnm"


def extract_text_from_pdf(pdf_file_path, page_number):
    with open(pdf_file_path, 'rb') as file:
        pdf = PdfReader(file)
        page = pdf.pages[page_number]
        text = page.extract_text()
        text = text.replace('\n', ' ')
        text = text.lower()
        for i in str_to_replace:
            text = text.replace(i, ' ')
        while '  ' in text:
            text = text.replace('  ', ' ')
        text = ' '.join([c for c in text.split() if len(c) > 1])
        while '  ' in text:
            text = text.replace('  ', ' ')
        return re.sub(r'[^а-яА-Я0-9\s]', '', text)


def get_text(pdf_file_path, page_number):
    page_number = page_number.replace(' ', '')
    if '-' not in page_number:
        return extract_text_from_pdf(pdf_file_path, int(page_number))
    else:
        start, finish = int(page_number.split('-')[0]), int(page_number.split('-')[1])
        start -= 1
        text = ''
        for i in range(start, finish):
            text += ' '
            text += extract_text_from_pdf(pdf_file_path, i)
        return text


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
            theme, pages = info[0], info[1]
            subject_info['sections'].append(theme)
            subject_info['pages_number_of_sections'].append(pages)
            text = get_text(['path'], pages)
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
            theme, pages = info[0], info[1]
            subject_info['sections'].append(theme)
            subject_info['pages_number_of_sections'].append(pages)
            text = get_text(obj['path'], pages)
            subject_info['text_of_sections'].append(text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append(obj['path'])
        print(subject_info)
        with open(get_path(json_name), "w") as file:
            json.dump(subject_info, file)

