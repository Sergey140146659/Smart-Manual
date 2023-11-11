import yaml
import re
import markdown
from bs4 import BeautifulSoup
import json
import os

from ml.db_creating.faq_db_create import faq_db_create
from ml.db_creating.faq_list_creating import faq_list_creating
from ml.request_processing.lemmatization import lemma_text
from ml.preprocessing_data.Articles_path import get_path
import Levenshtein


def faq_db_update():
    """
        При загрузке обновленного архива переносит сохраненные вопросы из раздела "F.A.Q" в новую базу данных.
        Перенос происходит следующим образом:
            Для каждой новой статьи ищется старая статья, текст которой минимально отличается(по расстоянию Левенштейна).
            Если по итогу минимальное расстояние Левенштейна > 50, то считается, что такой статьи раньше не было.
        """
    recorded_articles_faq = []
    header_faq = [""]
    if not os.path.exists(get_path("faq.json")):
        faq_db_create()
        faq_list_creating()
        return
    else:
        with open(get_path("faq.json"), 'r', encoding='utf-8') as f:

            try_article = json.load(f)
            if len(try_article["faq_text"]) == 0:
                faq_db_create()
                faq_list_creating()
                return
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

    def recursive_walk(folder_path, cnt=0):
        for root, dirs, files in os.walk(folder_path):
            if '.revs' in dirs:
                dirs.remove('.revs')
            for file_name in sorted(files):
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        faq_name = get_article_name(file_path)
                        if faq_name in recorded_articles_faq:
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
                            faq_combined_text += ' ' + header_faq[-1]
                            faq_combined_text += ' ' + lemma_text(header_faq[-1])
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
                        recorded_articles_faq.append(faq_name)
                        if len(faq_paragraphs) == 1 and "[ks-child-toc]" in faq_paragraphs[0]:
                            header_faq.append(faq_name)
                            continue
                        faq["faq_info"].append(faq_info)
                        for column, content in faq_info.items():
                            faq[column].append(content)
            for dir_name in sorted(dirs):
                recursive_walk(os.path.join(root, dir_name), cnt + 1)

    recursive_walk(folder_path)
    for i in range(len(faq["faq_name"])):
        faq["faq_index"][faq["faq_name"][i]] = i

    with open(get_path("faq.json"), 'r', encoding='utf-8') as f:
        old_faq = json.load(f)
    used_faqs = [0] * len(old_faq["faq_text"])

    for faq_i in range(len(faq["faq_text"])):
        used_pos = -1
        min_levenshtein_dist = 10 ** 9
        questions = []
        for old_faq_j in range(len(old_faq["faq_text"])):
            if used_faqs[old_faq_j] == 1:
                continue
            if min_levenshtein_dist == 0:
                break
            cur_dist = Levenshtein.distance(faq["faq_text"][faq_i], old_faq["faq_text"][old_faq_j])
            if cur_dist < min_levenshtein_dist:
                min_levenshtein_dist = cur_dist
                questions = old_faq["faq_questions"][old_faq_j]
                used_pos = old_faq_j
        if min_levenshtein_dist > 50:
            questions = []
            used_pos = -1
        faq["faq_questions"][faq_i] = questions
        if used_pos != -1:
            used_faqs[used_pos] = 1
        for question in questions:
            lemma_question = lemma_text(question)
            for i in range(6):
                faq["faq_combined_text"][faq_i] += ' ' + question
                faq["faq_combined_text"][faq_i] += ' ' + lemma_question
    with open(get_path("faq.json"), 'w', encoding='utf-8') as f:
        json.dump(faq, f)

    faq_list_creating()
