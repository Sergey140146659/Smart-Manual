import json

from ml.preprocessing_data.Articles_path import get_path
from ml.preprocessing_data.check_subject import check_sub
from ml.request_processing.lemmatization import lemma_text


def write_questions(obj):
    name = obj["name"]
    theme_name = obj["theme_name"]
    questions = obj["questions"]
    with open(get_path(obj['path']), 'r') as file:
        data = json.load(file)
    index = check_sub(name)
    json_name = data['json_name'][index]
    with open(get_path(json_name), 'r') as file:
        sub = json.load(file)
    for i in range(len(sub["sections"])):
        if sub["sections"] == theme_name:
            sub["questions"][i] = questions
            sub["lemma_questions"][i] = []
            for j in questions:
                sub["lemma_questions"][i].append(lemma_text(j))
            sub["combined_text_of_sections"][i] = sub['text_of_sections'][i] + ' ' + sub["lemma_text_of_sections"][i]
            for j in sub["lemma_questions"][i]:
                sub["combined_text_of_sections"][i] += ' '
                sub["combined_text_of_sections"][i] += j
            with open(get_path(json_name), 'w') as file:
                json.dump(sub, file)
            break
