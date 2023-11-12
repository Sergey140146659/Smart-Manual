import json

from classification.classifier_model import classifier
from random import randint

from ml.preprocessing_data.Articles_path import get_path
from ml.preprocessing_data.check_subject import check_sub
from ml.request_processing.request_reduction import request_processing

from ml.searching.search import searching_tf_idf_faq

dont_understand = ["Простите, я не уверен, что вы имеете в виду. Можете объяснить более подробно?",
                   "Извините, я не распознал ваш запрос. Можете повторить его?",
                   "Пожалуйста, уточните ваш запрос. Я могу быть более точной, если вы дадите мне больше информации.",
                   "Я извиняюсь, но я не понимаю вашего запроса. Можете сформулировать его иначе?"]

understand = [
    "Я нашел следующую информацию, которая может вам помочь:",
    "Вот что я нашел по вашему запросу:",
    "Вот что мне удалось найти для вас:",
    "Я нашел следующую информацию, которая, возможно, будет полезной:",
    "Вот что я нашел по вашей теме:",
    "Я нашел следующие результаты по вашему запросу:",
    "Вот что у меня есть на эту тему:"
]


def get_answer(subject, request):
    process_request = request_processing(request)
    request = request + ' ' + process_request
    with open(get_path('subjects.json'), 'r') as file:
        data = json.load(file)
    index = check_sub(subject)
    json_name = data['json_name'][index]
    subs = searching_tf_idf_faq(json_name, request)
    answer = []
    for sub in subs:
        pages = sub['pages_number_of_sections']
        page_start = 0
        page_end = 0
        page_number = pages.replace(' ', '')
        if '-' not in page_number:
            page_start = int(page_number)
            page_end = int(page_number)
        else:
            page_start, page_end = int(page_number.split('-')[0]), int(page_number.split('-')[1])
        answer.append({
            'theme_name': sub['sections'],
            'pdf_name': sub['path_to_pdf'],
            'page_start': page_start,
            'page_end': page_end
        })
    return answer
