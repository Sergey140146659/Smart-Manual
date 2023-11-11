from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from ml.preprocessing_data.Articles_path import get_path


def searching_tf_idf_faq(request, top_n=5):
    '''
     Функция использует сохраненный ранее корпус статей и матрицу TF-IDF для вычисления косинусной схожести между
     запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
     и возвращает их в виде списка словарей
    '''
    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        all_faq = json.load(f)

    combined_articles = all_faq["faq_combined_text"]
    combined_vectorizer = TfidfVectorizer()
    combined_matrix = combined_vectorizer.fit_transform(combined_articles)

    request_tfidf = combined_vectorizer.transform([request])
    cosine_similarities = cosine_similarity(request_tfidf, combined_matrix)
    indices = cosine_similarities.argsort()[0][-top_n:]
    faq = []
    for index in indices:
        faq_i = {
            "faq_name": all_faq["faq_name"][index],
            "faq_text": all_faq["faq_text"][index],
            "faq_lemma_text": all_faq["faq_lemma_text"][index],
            "faq_combined_text": all_faq["faq_combined_text"][index],
            "faq_link": all_faq["faq_link"][index],
            "faq_paragraphs": all_faq["faq_paragraphs"][index],
            "faq_lemma_paragraphs": all_faq["faq_lemma_paragraphs"][index],
            "faq_combined_paragraphs": all_faq["faq_combined_paragraphs"][index]
        }

        faq.append(faq_i)
    return faq


def searching_bm25_faq(request, top_n=5):
    '''
    Функция использует сохраненный ранее корпус статей и модель BM25 для вычисления баллов релевантности
    между запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
    и возвращает их в виде списка словарей.
    '''
    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        all_faq = json.load(f)
    combined_articles = all_faq["faq_combined_text"]
    tokenized_combined = [doc.split(" ") for doc in combined_articles]
    bm25_combined = BM25Okapi(tokenized_combined)
    tokenized_question = request.split(" ")
    doc_scores = bm25_combined.get_scores(tokenized_question)
    sorted_doc_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
    faq = []
    for index in sorted_doc_indices:
        faq_i = {
            "faq_name": all_faq["faq_name"][index],
            "faq_text": all_faq["faq_text"][index],
            "faq_lemma_text": all_faq["faq_lemma_text"][index],
            "faq_combined_text": all_faq["faq_combined_text"][index],
            "faq_link": all_faq["faq_link"][index],
            "faq_paragraphs": all_faq["faq_paragraphs"][index],
            "faq_lemma_paragraphs": all_faq["faq_lemma_paragraphs"][index],
            "faq_combined_paragraphs": all_faq["faq_combined_paragraphs"][index]
        }
        faq.append(faq_i)
    return faq
