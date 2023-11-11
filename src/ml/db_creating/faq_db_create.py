import yaml
import re
import markdown
from bs4 import BeautifulSoup

import json
import os
from ml.request_processing.lemmatization import lemma_text
from ml.preprocessing_data.Articles_path import get_path

recorded_articles_for_upd = []


def faq_db_create():
    """
    Функция faq_db_create() создает базу данных раздела "F.A.Q." в виде JSON-файла faq.json.
    Затем функция создает словарь faq, содержащий следующие ключи:
    faq_info: список словарей, каждый из которых содержит информацию о статье.
    faq_name: список названий статей.
    faq_text: список текстов статей.
    faq_lemma_text: список лемматизированных текстов статей.
    faq_combined_text: список текстов статей, объединенных с названиями заголовков и их лемматизированными версиями.
    faq_link: список ссылок на статьи.
    faq_paragraphs: список списков, каждый из которых содержит параграфы соответствующей статьи.
    faq_lemma_paragraphs: список списков, каждый из которых содержит лемматизированные версии параграфов соответствующей статьи.
    faq_combined_paragraphs: список списков, каждый из которых содержит параграфы соответствующей статьи, объединенные
    с лемматизированными версиями заголовков.
    faq_questions: список списков, каждый из которых содержит вопросы и ответы для соответствующей статьи.
    faq_index: словарь, который содержит соответствие между названием статьи и ее индексом в списке faq_info.
    """
    faq = {
        "faq_info": [

        ],
        "faq_name": [

        ],
        "faq_text": [

        ],
        "faq_lemma_text": [

        ],
        "faq_combined_text": [

        ],
        "faq_link": [

        ],
        "faq_paragraphs": [

        ],
        "faq_lemma_paragraphs": [

        ],
        "faq_combined_paragraphs": [

        ],
        "faq_questions": [

        ],
        "faq_index": {

        }
    }

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
            return text  # текст статьи

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

    def get_faq_link(path):
        s = path[path.find("f-a-q"):]
        s = s.replace("\\", '/')
        s = regex.sub('', s)
        s = remove_digits_and_lowercase(s)
        return beg + s

    folder_path = get_path("05.f-a-q")
    header_for_upd = [""]

    def recursive_walk_faq(folder_path, cnt=0):
        global recorded_articles_for_upd
        for root, dirs, files in os.walk(folder_path):
            if '.revs' in dirs:
                dirs.remove('.revs')
            for file_name in sorted(files):
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        faq_name = get_article_name(file_path)
                        if faq_name in recorded_articles_for_upd:
                            continue

                        faq_text = get_article_text(file_path)
                        faq_paragraphs = faq_text.split("\n")

                        faq_lemma_text = lemma_text(faq_text)
                        faq_lemma_paragraphs = [lemma_text(i) for i in faq_paragraphs]
                        faq_link = get_faq_link(root)
                        faq_combined_text = faq_text + ' ' + faq_lemma_text
                        faq_combined_paragraphs = [i + ' ' + j for i, j in zip(faq_paragraphs, faq_lemma_paragraphs)]
                        name = faq_name.replace("_", " ").replace(".", ' ').replace('-', ' ')
                        while '  ' in name:
                            name = name.replace("  ", ' ')
                        for i in range(5):
                            faq_combined_text += ' ' + name
                            faq_combined_text += ' ' + lemma_text(name)
                            faq_combined_text += ' ' + header_for_upd[-1]
                            faq_combined_text += ' ' + lemma_text(header_for_upd[-1])
                        faq_info = {
                            "faq_name": faq_name,
                            "faq_text": faq_text,
                            "faq_lemma_text": faq_lemma_text,
                            "faq_combined_text": faq_combined_text,
                            "faq_link": faq_link,
                            "faq_paragraphs": faq_paragraphs,
                            "faq_lemma_paragraphs": faq_lemma_paragraphs,
                            "faq_combined_paragraphs": faq_combined_paragraphs,
                            "faq_questions": []
                        }
                        recorded_articles_for_upd.append(faq_name)
                        if len(faq_paragraphs) == 1 and "[ks-child-toc]" in faq_paragraphs[0]:
                            header_for_upd.append(faq_name)
                            continue
                        faq["faq_info"].append(faq_info)

                        for column, content in faq_info.items():
                            faq[column].append(content)
            for dir_name in sorted(dirs):
                recursive_walk_faq(os.path.join(root, dir_name), cnt + 1)

    recursive_walk_faq(folder_path)
    for i in range(len(faq["faq_name"])):
        faq["faq_index"][faq["faq_name"][i]] = i
    with open(get_path("faq.json"), 'w', encoding='utf-8') as f:
        json.dump(faq, f)
