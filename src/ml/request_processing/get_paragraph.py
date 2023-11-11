import json

from ml.preprocessing_data.Articles_path import get_path

with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
    all_articles = json.load(f)

with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
    all_faqs = json.load(f)


def get_important_paragraphs_article(article_info):
    '''
    Возвращает первые несколько абзацев статьи(из раздела "2. Описание операций"), которые в сумме содержат не более 270 символов.
    '''
    end = 0
    summary_symbol = 0
    while summary_symbol < 270 and end < len(article_info["article_paragraphs"]):
        summary_symbol += len(article_info["article_paragraphs"][end])
        end += 1

    return '\n'.join(article_info["article_paragraphs"][0: end])


def get_important_paragraphs_faq(faq_info):
    '''
    Возвращает первые несколько абзацев статьи(из раздела "F.A.Q"), которые в сумме содержат не более 270 символов.
    '''
    end = 0
    summary_symbol = 0
    while summary_symbol < 270 and end < len(faq_info["faq_paragraphs"]):
        summary_symbol += len(faq_info["faq_paragraphs"][end])
        end += 1

    return '\n'.join(faq_info["faq_paragraphs"][0: end])
