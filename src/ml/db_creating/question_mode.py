import json

from ml.request_processing.lemmatization import lemma_text


def write_questions(obj):
    name = obj["name"]
    questions = obj["questions"]
    with open("subjects.json", 'r') as file:
        subjects = json.load(file)
    for i in range(len(subjects["json_name"])):
        if subjects["orig_name"][i] == name:
            subjects["questions"][i] = questions
            subjects["lemma_questions"][i] = []
            for j in questions:
                subjects["lemma_questions"][i].append(lemma_text(j))
            break