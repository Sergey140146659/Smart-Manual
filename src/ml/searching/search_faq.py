from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from ml.preprocessing_data.Articles_path import get_path


def searching_tf_idf_faq(path, request, top_n=5):
    '''
     Функция использует сохраненный ранее корпус статей и матрицу TF-IDF для вычисления косинусной схожести между
     запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
     и возвращает их в виде списка словарей
    '''
    with open(get_path(path), 'r', encoding='utf-8') as f:
        subject = json.load(f)

    combined_articles = subject["combined_text_of_sections"]
    combined_vectorizer = TfidfVectorizer()
    combined_matrix = combined_vectorizer.fit_transform(combined_articles)

    request_tfidf = combined_vectorizer.transform([request])
    cosine_similarities = cosine_similarity(request_tfidf, combined_matrix)
    indices = cosine_similarities.argsort()[0][-top_n:]
    subject = []
    for index in indices:
        subject_i = {
            "sections": subject["sections"][index],
            "pages_number_of_sections": subject["pages_number_of_sections"][index],
            "text_of_sections": subject["text_of_sections"][index],
            "lemma_text_of_sections": subject["lemma_text_of_sections   "][index],
            "combined_text_of_sections": subject["combined_text_of_sections"][index],
            "path_to_pdf": subject["path_to_pdf"][index]
        }

        subject.append(subject_i)
    return subject


def searching_bm25_faq(path, request, top_n=5):
    '''
    Функция использует сохраненный ранее корпус статей и модель BM25 для вычисления баллов релевантности
    между запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
    и возвращает их в виде списка словарей.
    '''
    with open(get_path(path), 'r', encoding='utf-8') as f:
        subject = json.load(f)
    combined_articles = subject["combined_text_of_sections"]
    tokenized_combined = [doc.split(" ") for doc in combined_articles]
    bm25_combined = BM25Okapi(tokenized_combined)
    tokenized_question = request.split(" ")
    doc_scores = bm25_combined.get_scores(tokenized_question)
    sorted_doc_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
    subject = []
    for index in sorted_doc_indices:
        subject_i = {
            "sections": subject["sections"][index],
            "pages_number_of_sections": subject["pages_number_of_sections"][index],
            "text_of_sections": subject["text_of_sections"][index],
            "lemma_text_of_sections": subject["lemma_text_of_sections   "][index],
            "combined_text_of_sections": subject["combined_text_of_sections"][index],
            "path_to_pdf": subject["path_to_pdf"][index]
        }

        subject.append(subject_i)
    return subject
