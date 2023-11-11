from classification.classifier_model import classifier
from random import randint
from ml.request_processing.get_paragraph import get_important_paragraphs_faq, get_important_paragraphs_article
from ml.request_processing.request_reduction import request_processing

from ml.searching.search_article import searching_tf_idf, searching_bm25
from ml.searching.search_faq import searching_tf_idf_faq, searching_bm25_faq
from ml.searching.search_law223 import unite_laws223
from ml.searching.search_law44 import unite_laws44

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


def unite_articles(articles_tf, articles_bm):
    '''
    Эта функция объединяет результаты поиска по законам с помощью методов BM25 и TF-IDF
    для определения наиболее релевантных законов по запросу.
    Если два метода поиска вернули одинаковые законы, то они не будут дублироваться в итоговом списке.
    '''
    articles_togetger = []
    for a, b in zip(articles_bm, articles_tf):
        if a != b:
            if a not in articles_togetger:
                articles_togetger.append(a)
            if b not in articles_togetger:
                articles_togetger.append(b)
        else:
            if a not in articles_togetger:
                articles_togetger.append(a)
    return articles_togetger[0: min(len(articles_togetger), 5)]


faq_keys = ["faq_text", 'faq_lemma_text', 'faq_combined_text', 'faq_paragraphs',
            'faq_lemma_paragraphs', 'faq_combined_paragraphs']


def faq_answer(request):
    '''
    Эта функция предназначена для ответа на вопросы в разделе FAQ.
    Формирует словарь ответа на вопрос, который содержит информацию о наиболее релевантном ответе,
    комментарии и список других возможных ответов на вопросы.
    '''
    faq_tf = searching_tf_idf_faq(request)
    faq_bm = searching_bm25_faq(request)
    faq_together = unite_articles(faq_tf, faq_bm)
    text = get_important_paragraphs_faq(faq_together[0])
    for i in range(len(faq_together)):
        for j in faq_keys:
            del faq_together[i][j]
    comment = ["Подробнее можете ознакомиться:", "Также может быть полезно:"]
    answer = {"text_paragraphs": text, "main_faq": faq_together[0],
              "comment": comment,
              "faqs": faq_together[1:]}
    return answer


article_keys = ['article_text', 'article_lemma_text', 'article_combined_text',
                'article_paragraphs', 'article_lemma_paragraphs', 'article_combined_paragraphs']


def article_answer(request):
    '''
    Эта функция предназначена для ответа на вопросы в разделе Описание операций.
    Формирует словарь ответа на вопрос, который содержит информацию о наиболее релевантном ответе,
    комментарии и список других возможных ответов на вопросы.
    '''
    articles_tf = searching_tf_idf(request)
    articles_bm = searching_bm25(request)
    articles_together = unite_articles(articles_tf, articles_bm)
    text_paragraphs = get_important_paragraphs_article(articles_together[0])
    for i in range(len(articles_together)):
        for j in article_keys:
            del articles_together[i][j]
    comment = ["Подробнее можете ознакомиться:", "Также может быть полезно:"]
    answer = {"text_paragraphs": text_paragraphs, "main_article": articles_together[0], "comment": comment,
              "articles": articles_together[1:]}
    return answer


law_keys = ["law_text", "law_lemma_text", "law_combined_text"]


def laws_answer(request):
    '''
    Эта функция предназначена для ответа на вопросы, связанные с законодательством.
    Формирует словарь ответа, который содержит список наиболее релевантных законов.
    '''
    laws44 = unite_laws44(request)
    laws223 = unite_laws223(request)
    laws = []
    for a, b in zip(laws44, laws223):
        if a != b:
            if a not in laws:
                laws.append(a)
            if b not in laws:
                laws.append(b)
        else:
            if a not in laws:
                laws.append(a)
    for i in range(len(laws)):
        for j in law_keys:
            del laws[i][j]
    answer = {"laws": laws[0: min(len(laws), 5)]}
    return answer


def answer_user_question(request, questions):
    process_request = request_processing(request)
    request = request + ' ' + process_request
    if classifier(process_request) == 0 or process_request == '':
        return {
            "is_valid": 0,
            "comment": dont_understand[randint(0, len(dont_understand) - 1)],
            "ans": {
                "faq": None,
                "article": None,
                "law": None
            }
        }
    return {
        "is_valid": 1,
        "comment": "",
        "ans": {
            "faq": faq_answer(request) if questions["faq"] else None,
            "article": article_answer(request) if questions["article"] else None,
            "law": laws_answer(request) if questions["law"] else None
        }
    }


def get_answer(request, questions):
    process_request = request_processing(request)
    request = request + ' ' + process_request
    return {
        "is_valid": 1,
        "comment": "",
        "ans": {
            "faq": faq_answer(request) if questions["faq"] else None,
            "article": article_answer(request) if questions["article"] else None,
            "law": laws_answer(request) if questions["law"] else None
        }
    }
