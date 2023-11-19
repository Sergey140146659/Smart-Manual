import json

from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text


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


def clear(text):
    for i in '0123456789':
        text = text.replace(i, ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    text = text.split(' ')
    new_text = []
    for i in text:
        if len(i) > 2:
            new_text.append(i)
    return ' '.join(new_text)


with open(get_path("subjects.json"), 'r') as file:
    data = json.load(file)
for sub in data["json_name"]:
    with open(get_path(sub), 'r') as file:
        subject = json.load(file)
    for i in range(len(subject["text_of_sections"])):
        subject["text_of_sections"][i] = clear(subject["text_of_sections"][i])
        subject["lemma_text_of_sections"][i] = lemma_text(subject["lemma_text_of_sections"][i])
        subject["combined_text_of_sections"][i] = subject["text_of_sections"][i] + ' ' + \
                                                  subject["lemma_text_of_sections"][i]

    with open(get_path(sub), 'w') as file:
        json.dump(subject, file)
