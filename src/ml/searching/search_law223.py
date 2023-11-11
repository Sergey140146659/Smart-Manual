import pickle

from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from ml.preprocessing_data.Articles_path import get_path


def searching_bm25_law223(request, top_n=5):
    '''
    Функция использует сохраненный ранее корпус статей и модель BM25 для вычисления баллов релевантности
    между запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
    и возвращает их в виде списка словарей.
    '''

    with open(get_path('laws223.json'), 'r', encoding='utf-8') as f:
        laws223 = json.load(f)
    combined_articles = laws223["law_combined_text"]
    tokenized_combined = [doc.split(" ") for doc in combined_articles]
    bm25_combined = BM25Okapi(tokenized_combined)
    tokenized_question = request.split(" ")
    doc_scores = bm25_combined.get_scores(tokenized_question)
    sorted_doc_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
    law = []
    for index in sorted_doc_indices:
        law_i = {
            "law_name": f'ФЗ-223: {laws223["law_name"][index]}',
            "law_text": laws223["law_text"][index],
            "law_lemma_text": laws223["law_lemma_text"][index],
            "law_combined_text": laws223["law_combined_text"][index],
            "law_link": laws223["law_link"][index],

        }
        law.append(law_i)
    return law


def searching_tf_idf_law223(request, top_n=5):
    '''
     Функция использует сохраненный ранее корпус статей и матрицу TF-IDF для вычисления косинусной схожести между
     запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
     и возвращает их в виде списка словарей
    '''
    with open(get_path('laws223.json'), 'r', encoding='utf-8') as f:
        laws223 = json.load(f)
    combined_articles = laws223["law_combined_text"]
    combined_vectorizer = TfidfVectorizer()
    combined_matrix = combined_vectorizer.fit_transform(combined_articles)
    request_tfidf = combined_vectorizer.transform([request])
    cosine_similarities = cosine_similarity(request_tfidf, combined_matrix)
    indices = cosine_similarities.argsort()[0][-top_n:]
    law = []
    for index in indices:
        law_i = {
            "law_name": f'ФЗ-223: {laws223["law_name"][index]}',
            "law_text": laws223["law_text"][index],
            "law_lemma_text": laws223["law_lemma_text"][index],
            "law_combined_text": laws223["law_combined_text"][index],
            "law_link": laws223["law_link"][index],

        }
        law.append(law_i)
    return law


def unite_laws223(request):
    '''
    Эта функция объединяет результаты поиска по законам с помощью методов BM25 и TF-IDF
    для определения наиболее релевантных законов по запросу.
    Если два метода поиска вернули одинаковые законы, то они не будут дублироваться в итоговом списке.
    '''
    laws_bm = searching_bm25_law223(request)
    laws_tf = searching_tf_idf_law223(request)
    laws_togetger = []
    for a, b in zip(laws_bm, laws_tf):
        if a != b:
            if a not in laws_togetger:
                laws_togetger.append(a)
            if b not in laws_togetger:
                laws_togetger.append(b)
        else:
            if a not in laws_togetger:
                laws_togetger.append(a)
    return laws_togetger[0: min(len(laws_togetger), 5)]
