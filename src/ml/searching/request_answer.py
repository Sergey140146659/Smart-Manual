from classification.classifier_model import classifier
from random import randint
from ml.request_processing.request_reduction import request_processing

from ml.searching.search_article import searching_tf_idf, searching_bm25
from ml.searching.search_faq import searching_tf_idf_faq, searching_bm25_faq


dont_understand = ["Простите, я не уверен, что вы имеете в виду. Можете объяснить более подробно?",
                   "Извините, я не распознал ваш запрос. Можете повторить его?",
                   "Пожалуйста, уточните ваш запрос. Я могу быть более точной, если вы дадите мне больше информации.",
                   "Я извиняюсь, но я не понимаю вашего запроса. Можете сформулировать его иначе?"]

understand =  [
    "Я нашел следующую информацию, которая может вам помочь:",
    "Вот что я нашел по вашему запросу:",
    "Вот что мне удалось найти для вас:",
    "Я нашел следующую информацию, которая, возможно, будет полезной:",
    "Вот что я нашел по вашей теме:",
    "Я нашел следующие результаты по вашему запросу:",
    "Вот что у меня есть на эту тему:"
]

