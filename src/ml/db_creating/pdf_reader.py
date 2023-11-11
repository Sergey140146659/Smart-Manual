import json

from PyPDF2 import PdfReader

from ml.request_processing.lemmatization import lemma_text
from src.ml.preprocessing_data.check_subject import check_sub

str_to_replace = "!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–"
replace_dict = str.maketrans(str_to_replace, ' ' * len(str_to_replace))


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
        return text


def get_text(pdf_file_path, page_number):
    page_number = page_number.replace(' ', '')
    if '-' not in page_number:
        return extract_text_from_pdf(pdf_file_path, page_number)
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
    if check_sub(obj['name']):
        with open('subjects.json', 'r') as file:
            data = json.load(file)
        json_name = data['subjects'][obj['name']]
        with open(json_name, 'r') as file:
            subject_info = json.load(file)
        for theme, pages in obj['themes']:
            subject_info['sections'].append(theme)
            subject_info['pages_number_of_sections'].append(pages)
            text = get_text("PATH_TO_PDF", pages)
            subject_info['text_of_sections'].append(get_text)
            lemma = lemma_text(text)
            subject_info['lemma_text_of_sections'].append(lemma)
            subject_info['combined_text_of_sections'].append(lemma + ' ' + text)
            subject_info['path_to_pdf'].append("PATH_TO_PDF")
    else:
        with open("данные.json", "w") as file:
            pass

    pass
