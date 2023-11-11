import json

from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text


def get_question_list(name):
    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        faq = json.load(f)
    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        articles = json.load(f)
    type = "faq" if name in faq["faq_index"] else "article"
    index = faq["faq_index"][name] if type == "faq" else articles["article_index"][name]
    if type == "faq":
        return faq["faq_questions"][index]
    if type == "article":
        return articles["article_questions"][index]


def update_question_list(name, questions):
    '''
    Она принимает имя статьи или вопроса и список вопросов, которые необходимо добавить.
    Затем она загружает соответствующий файл JSON (faq.json или articles.json) и находит индекс для указанного имени.
    Затем функция добавляет новые вопросы в список вопросов для статьи или вопроса, обновляет комбинированный текст для
    статьи, который используется для поиска, и сохраняет изменения в файл JSON.

    Если обновляется список вопросов для раздела FAQ, функция также вызывает функцию creating_matrix_tf_and_bm_faq,
    чтобы пересоздать матрицы TF-IDF и BM25 для поиска по разделу FAQ.

    Если обновляется список вопросов для статьи, функция вызывает функцию creating_matrix_tf_and_bm_articles,
    чтобы пересоздать матрицы TF-IDF и BM25 для поиска по статьям.
    '''
    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        faq = json.load(f)
    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        articles = json.load(f)
    type = "faq" if name in faq["faq_index"] else "article"
    index = faq["faq_index"][name] if type == "faq" else articles["article_index"][name]
    if type == "faq":
        faq["faq_questions"][index] = []
        faq["faq_combined_text"][index] = faq["faq_text"][index] + ' ' + faq["faq_lemma_text"][index]
        for question in questions:
            lemma_question = lemma_text(question)
            faq["faq_questions"][index].append(question)
            for i in range(6):
                faq["faq_combined_text"][index] += ' ' + question
                faq["faq_combined_text"][index] += ' ' + lemma_question
        with open(get_path("faq.json"), 'w', encoding='utf-8') as f:
            json.dump(faq, f)

    if type == "article":
        articles["article_combined_text"][index] = articles["article_text"][index] + ' ' + \
                                                   articles["article_lemma_text"][index]
        articles["article_questions"][index] = []
        for question in questions:
            lemma_question = lemma_text(question)
            articles["article_questions"][index].append(question)
            for i in range(6):
                articles["article_combined_text"][index] += ' ' + question
                articles["article_combined_text"][index] += ' ' + lemma_question
        with open(get_path("articles.json"), 'w', encoding='utf-8') as f:
            json.dump(articles, f)
