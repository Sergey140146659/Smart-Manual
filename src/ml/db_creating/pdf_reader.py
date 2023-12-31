import re

from PyPDF2 import PdfReader

from ml.preprocessing_data.Articles_path import get_path

str_to_replace = "!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–qwertyiopasdfghjklzxcvbnm0123456789"


def extract_text_from_pdf(pdf_file_path, page_number):
    with open(get_path(pdf_file_path), 'rb') as file:
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


def get_text(pdf_file_path, page_start, page_end):
    start, finish = page_start, page_end
    start -= 1
    text = ''
    for i in range(start, finish):
        text += ' '
        text += extract_text_from_pdf(pdf_file_path, i)
    return text
