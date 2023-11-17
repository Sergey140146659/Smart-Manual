import json

from ml.preprocessing_data.Articles_path import get_path
from ml.preprocessing_data.check_subject import check_sub
from ml.request_processing.lemmatization import lemma_text


def write_note(name, theme_name, questions):
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)

    index = check_sub(name)
    json_name = data['json_name'][index]
    with open(get_path(json_name), 'r') as file:
        sub = json.load(file)
    for i in range(len(sub["sections"])):
        if sub["sections"][i] == theme_name:
            sub["questions"][i] = questions
            sub["lemma_questions"][i] = lemma_text(questions)
            sub["combined_text_of_sections"][i] = sub['text_of_sections'][i] + ' ' + sub["lemma_text_of_sections"][i] + \
                                                  ' ' + sub["questions"][i] + ' ' + sub["lemma_questions"][i]
            with open(get_path(json_name), 'w') as file:
                json.dump(sub, file)
            break


def get_note(name, theme_name):
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)

    index = check_sub(name)
    json_name = data['json_name'][index]
    with open(get_path(json_name), 'r') as file:
        sub = json.load(file)
    for i in range(len(sub["sections"])):
        if sub["sections"][i] == theme_name:
            return sub["questions"][i]
