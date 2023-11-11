import json

from ml.request_processing.lemmatization import lemma_text
from ml.preprocessing_data.Articles_path import get_path


def add_question(data_for_db_update):
    """
    Добавляет новые вопросы в соответствующие статьи базы данных.

    Аргумент data_for_db_update - список словарей, каждый из которых содержит название статьи и текст вопроса.

    Для каждого словаря в списке data_for_db_update функция извлекает название статьи и текст вопроса.
    Затем функция проверяет, относится ли статья к разделу "Вопросы и ответы" (FAQ) или к разделу статей.

    Далее функция определяет индекс статьи в соответствующем списке и проверяет, есть ли такой вопрос уже в базе данных.
    Если вопрос уже есть, то функция переходит к следующему вопросу.

    Если же вопроса еще нет в базе данных, то функция добавляет его в соответствующий список вопросов
    и обновляет текстовое представление списка вопросов для этой статьи.

    В конце функция сохраняет изменения в файлах faq.json и articles.json.
    """
    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        faq = json.load(f)
    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        articles = json.load(f)
    for article in data_for_db_update:
        name = article["article_name"]
        question = article["query"]
        lemma_question = lemma_text(question)
        type = "faq" if name in faq["faq_index"] else "article"
        index = faq["faq_index"][name] if type == "faq" else articles["article_index"][name]
        if type == "faq":
            if question in faq["faq_questions"][index]:
                continue
            faq["faq_questions"][index].append(question)
            for i in range(6):
                faq["faq_combined_text"][index] += ' ' + question
                faq["faq_combined_text"][index] += ' ' + lemma_question
            with open(get_path("faq.json"), 'w', encoding='utf-8') as f:
                json.dump(faq, f)
        if type == "article":
            if question in articles["article_questions"][index]:
                continue
            articles["article_questions"][index].append(question)
            for i in range(6):
                articles["article_combined_text"][index] += ' ' + question
                articles["article_combined_text"][index] += ' ' + lemma_question
            with open(get_path("articles.json"), 'w', encoding='utf-8') as f:
                json.dump(articles, f)

