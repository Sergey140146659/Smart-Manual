import os
import pickle
import re

import markdown
import yaml
from bs4 import BeautifulSoup

from ml.preprocessing_data.Articles_path import get_path


def article_list_creating():
    """
    Создает структуру вложенных списков из заголовков статей раздела "2. Описание операций"
    Пример:
    [{'name': '2. Описание операций', 'is_parent': True},
        [
        {'name': '2.1. Вход в комплекс', 'is_parent': False},
        {'name': '2.2. Основные настройки системы', 'is_parent': True},
            [
            {'name': '2.2.1. Настройка расчетного периода', 'is_parent': False},
            ...
            {'name': '2.2.9. Настройка взаимодействия с сервисами ЕИС', 'is_parent': False}
            ]
        ]
    ]
    """

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

    recorded_articles_list_article = []
    headers_list_article = []
    nested_list_article = []

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
                        if article_name in recorded_articles_list_article:
                            continue
                        recorded_articles_list_article.append(article_name)
                        article_text = get_article_text(file_path)
                        article_paragraphs = article_text.split("\n")
                        nested_list_article.append((article_name, cnt))
                        if sum([("[ks-child-toc]" in i) for i in article_paragraphs]):
                            headers_list_article.append(article_name)

                        if len(article_paragraphs) == 1 and "[ks-child-toc]" in article_paragraphs[0]:
                            continue

                        recorded_articles_list_article.append(article_name)

            for dir_name in sorted(dirs):
                recursive_walk(os.path.join(root, dir_name), cnt + 1)

    recursive_walk(folder_path)

    def update(nested):
        for i in range(len(nested)):
            if isinstance(nested[i], str):
                nested[i] = {"name": nested[i], "is_parent": nested[i] in headers_list_article}
            else:
                update(nested[i])

    def article_list(nested):
        ans = []
        for i in range(len(nested)):
            cnt = nested[i][1]
            if cnt == 0:
                ans.append(nested[i][0])
                continue
            cur = ans
            cur_pr = ans
            for j in range(cnt):
                cur = cur[-1]
            for j in range(cnt - 1):
                cur_pr = cur_pr[-1]
            if isinstance(cur, list):
                cur.append(nested[i][0])
            else:
                cur_pr.append([nested[i][0]])
        update(ans)
        return ans

    res = article_list(nested_list_article)
    with open(get_path('article_list.pkl'), 'wb') as f:
        pickle.dump(res, f)
