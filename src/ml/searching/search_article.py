from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from ml.preprocessing_data.Articles_path import get_path


def searching_tf_idf(request, top_n=5):
    '''
     Функция использует сохраненный ранее корпус статей и матрицу TF-IDF для вычисления косинусной схожести между
     запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
     и возвращает их в виде списка словарей
    '''
    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        all_articles = json.load(f)
    combined_articles = all_articles["article_combined_text"]
    combined_vectorizer = TfidfVectorizer()
    combined_matrix = combined_vectorizer.fit_transform(combined_articles)

    request_tfidf = combined_vectorizer.transform([request])
    cosine_similarities = cosine_similarity(request_tfidf, combined_matrix)
    indices = cosine_similarities.argsort()[0][-top_n:]
    articles = []
    for index in indices:
        article = {"article_name": all_articles["article_name"][index],
                   "article_text": all_articles["article_text"][index],
                   "article_lemma_text": all_articles["article_lemma_text"][index],
                   "article_combined_text": all_articles["article_combined_text"][index],
                   "article_link": all_articles["article_link"][index],
                   "article_paragraphs": all_articles["article_paragraphs"][index],
                   "article_lemma_paragraphs": all_articles["article_lemma_paragraphs"][index],
                   "article_combined_paragraphs": all_articles["article_combined_paragraphs"][index]}
        articles.append(article)
    return articles


def searching_bm25(request, top_n=5):
    '''
    Функция использует сохраненный ранее корпус статей и модель BM25 для вычисления баллов релевантности
    между запросом и каждой статьей в корпусе. Затем она выбирает top_n наиболее релевантных статей
    и возвращает их в виде списка словарей.
    '''
    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        all_articles = json.load(f)
    combined_articles = all_articles["article_combined_text"]
    tokenized_combined = [doc.split(" ") for doc in combined_articles]
    bm25_combined = BM25Okapi(tokenized_combined)

    tokenized_question = request.split(" ")
    doc_scores = bm25_combined.get_scores(tokenized_question)
    sorted_doc_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_n]
    articles = []
    for index in sorted_doc_indices:
        article = {"article_name": all_articles["article_name"][index],
                   "article_text": all_articles["article_text"][index],
                   "article_lemma_text": all_articles["article_lemma_text"][index],
                   "article_combined_text": all_articles["article_combined_text"][index],
                   "article_link": all_articles["article_link"][index],
                   "article_paragraphs": all_articles["article_paragraphs"][index],
                   "article_lemma_paragraphs": all_articles["article_lemma_paragraphs"][index],
                   "article_combined_paragraphs": all_articles["article_combined_paragraphs"][index]}
        articles.append(article)
    return articles
