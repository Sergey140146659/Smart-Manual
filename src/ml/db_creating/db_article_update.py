import yaml
import re
import markdown
from bs4 import BeautifulSoup
import os
import json

from ml.db_creating.article_list_creating import article_list_creating
from ml.db_creating.articles_db_create import article_db_create
from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text
import Levenshtein


def article_db_update():
    """
    При загрузке обновленного архива переносит сохраненные вопросы из раздела "Описание операций" в новую базу данных.
    Перенос происходит следующим образом:
        Для каждой новой статьи ищется старая статья, текст которой минимально отличается(по расстоянию Левенштейна).
        Если по итогу минимальное расстояние Левенштейна > 50, то считается, что такой статьи раньше не было.
    """
    recorded_articles_article = []
    headers_article = []
    if not os.path.exists(get_path("articles.json")):
        article_db_create()
        article_list_creating()
        return
    else:
        with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
            try_article = json.load(f)
            if len(try_article["article_text"]) == 0:
                article_db_create()
                article_list_creating()
                return

    articles = {
        "article_info": [

        ],
        "article_name": [

        ],
        "article_text": [

        ],
        "article_lemma_text": [

        ],
        "article_combined_text": [

        ],
        "article_link": [

        ],
        "article_paragraphs": [

        ],
        "article_lemma_paragraphs": [

        ],
        "article_combined_paragraphs": [

        ],
        "article_questions": [

        ]
        ,
        "article_index": {

        }

    }

    folder_path = get_path("03.complex-operations")

    def get_article_name(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            yaml_data = f.read().split('---')[1].strip()
            metadata = yaml.safe_load(yaml_data)
            title = metadata['title']
            if title[-1] == ' ':
                title = title[:-1]
            return title  # получить название

    def get_article_text(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
            text = re.sub(r'^---.*---\n', '', text, flags=re.DOTALL)
            html_text = markdown.markdown(text)
            soup = BeautifulSoup(html_text, 'html.parser')
            text = soup.get_text()
            text = re.sub(r'{.*}', '', text)
            while "\n\n" in text:
                text = text.replace("\n\n", "\n")
            while "  " in text:
                text = text.replace("  ", " ")
            text = text.replace(" »", '»')
            return text

    def f(num):
        if num < 10:
            return "0" + str(num) + "."
        return str(num) + "."

    def remove_digits_and_lowercase(input_string):
        result = ''
        for char in input_string:
            result += char.lower()
        return result

    nums = [f(i) for i in range(0, 10000)]
    regex = re.compile('|'.join(map(re.escape, nums)))
    beg = "https://helpgznext.keysystems.ru/ru/"

    def get_article_link(path):
        s = path[path.find("complex-operations"):]
        s = s.replace("\\", '/')
        s = regex.sub('', s)
        s = remove_digits_and_lowercase(s)
        return beg + s

    def common_prefix(str1, str2):
        prefix = 0
        for i in range(min(len(str1), len(str2))):
            if str1[i] == str2[i]:
                prefix += 1
            else:
                break
        return prefix

    def recursive_walk(folder_path, cnt=0):
        for root, dirs, files in os.walk(folder_path):
            if '.revs' in dirs:
                dirs.remove('.revs')
            for file_name in sorted(files):
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        article_name = get_article_name(file_path).replace("\t", ' ')
                        while "  " in article_name:
                            article_name = article_name.replace("  ", " ")
                        article_name = article_name.strip()
                        if article_name in recorded_articles_article:
                            continue
                        recorded_articles_article.append(article_name)
                        article_text = get_article_text(file_path)
                        article_link = get_article_link(root)
                        article_paragraphs = article_text.split("\n")
                        article_lemma_text = lemma_text(article_text)
                        article_lemma_paragraphs = [lemma_text(i) for i in article_paragraphs]
                        article_combined_text = article_text + ' ' + article_lemma_text
                        article_lemma_name = lemma_text(article_name)
                        for i in range(5):
                            article_combined_text += ' ' + article_name
                            article_combined_text += ' ' + article_lemma_name

                        article_combined_paragraphs = [i + ' ' + j for i, j in
                                                       zip(article_paragraphs, article_lemma_paragraphs)]
                        article_info = {
                            "article_name": article_name,
                            "article_text": article_text,
                            "article_lemma_text": article_lemma_text,
                            "article_combined_text": article_combined_text,
                            "article_link": article_link,
                            "article_paragraphs": article_paragraphs,
                            "article_lemma_paragraphs": article_lemma_paragraphs,
                            "article_combined_paragraphs": article_combined_paragraphs,
                            "article_questions": []
                        }

                        if sum([("[ks-child-toc]" in i) for i in article_paragraphs]):
                            headers_article.append(article_name)

                        if len(article_paragraphs) == 1 and "[ks-child-toc]" in article_paragraphs[0]:
                            continue

                        recorded_articles_article.append(article_name)
                        for column, content in article_info.items():
                            articles[column].append(content)

            for dir_name in sorted(dirs):
                recursive_walk(os.path.join(root, dir_name), cnt + 1)

    recursive_walk(folder_path)
    for i in range(len(articles["article_name"])):

        articles["article_index"][articles["article_name"][i]] = i
        common_prefs = [common_prefix(articles["article_name"][i], headers_article[j]) for j in
                        range(len(headers_article))]
        for j in range(len(common_prefs)):
            if common_prefs[j] > 3:
                articles["article_combined_text"][i] += ' ' + headers_article[j]
                articles["article_combined_text"][i] += ' ' + lemma_text(headers_article[j])
        article_info = {
            "article_name": articles["article_name"][i],
            "article_text": articles["article_text"][i],
            "article_lemma_text": articles["article_lemma_text"][i],
            "article_combined_text": articles["article_combined_text"][i],
            "article_link": articles["article_link"][i],
            "article_paragraphs": articles["article_paragraphs"][i],
            "article_lemma_paragraphs": articles["article_lemma_paragraphs"][i],
            "article_combined_paragraphs": articles["article_combined_paragraphs"][i]
        }
        articles["article_info"].append(article_info)

    with open(get_path("articles.json"), 'r', encoding='utf-8') as f:
        old_article = json.load(f)
    used_articles = [0] * len(old_article["article_text"])
    for article_i in range(len(articles["article_text"])):
        used_pos = -1
        min_levenshtein_dist = 10 ** 9
        questions = []
        for old_article_i in range(len(old_article["article_text"])):
            if used_articles[old_article_i] == 1:
                continue
            if min_levenshtein_dist == 0:
                break
            cur_dist = Levenshtein.distance(articles["article_text"][article_i],
                                            old_article["article_text"][old_article_i])
            if cur_dist < min_levenshtein_dist:
                min_levenshtein_dist = cur_dist
                questions = old_article["article_questions"][old_article_i]
                used_pos = old_article_i
        if min_levenshtein_dist > 50:
            questions = []
            used_pos = -1

        articles["article_questions"][article_i] = questions

        if used_pos != -1:
            used_articles[used_pos] = 1
        for question in questions:
            lemma_question = lemma_text(question)
            for i in range(6):
                articles["article_combined_text"][article_i] += ' ' + question
                articles["article_combined_text"][article_i] += ' ' + lemma_question

    with open(get_path("articles.json"), 'w', encoding='utf-8') as f:
        json.dump(articles, f)
    article_list_creating()
