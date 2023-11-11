import pickle
import yaml
import re
import markdown
from bs4 import BeautifulSoup
import os
from ml.preprocessing_data.Articles_path import get_path


def faq_list_creating():
    """
       Создает структуру вложенных списков из заголовков статей раздела "F.A.Q"
       Пример:
       [{'name': 'F.A.Q. Часто задаваемые вопросы', 'is_parent': True},
           [
           {'name': 'План-график закупок', 'is_parent': True},
               [
               {'name': 'ПГ_ИК_6005', 'is_parent': False},
               {'name': 'Password check for user with login', 'is_parent': False},
               ...
               {'name': 'ПГ_ИК_4003', 'is_parent': False}
               ]
           ]
       ]
       """
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

    folder_path = get_path("05.f-a-q")

    nested_list_faq = []
    recorded_articles_list_faq = []
    header_list_faq = []

    def recursive_walk(folder_path, cnt=0):
        for root, dirs, files in os.walk(folder_path):
            if '.revs' in dirs:
                dirs.remove('.revs')
            for file_name in sorted(files):
                if file_name.endswith('.md'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        faq_name = get_article_name(file_path)
                        if faq_name in recorded_articles_list_faq:
                            continue
                        faq_text = get_article_text(file_path)
                        faq_paragraphs = faq_text.split("\n")
                        name = faq_name.replace("_", " ").replace(".", ' ').replace('-', ' ')
                        while '  ' in name:
                            name = name.replace("  ", ' ')
                        recorded_articles_list_faq.append(faq_name)
                        nested_list_faq.append((faq_name, cnt))
                        if len(faq_paragraphs) == 1 and "[ks-child-toc]" in faq_paragraphs[0]:
                            header_list_faq.append(faq_name)
                            continue
            for dir_name in sorted(dirs):
                recursive_walk(os.path.join(root, dir_name), cnt + 1)

    recursive_walk(folder_path)

    def update(nested):
        for i in range(len(nested)):
            if isinstance(nested[i], str):
                nested[i] = {"name": nested[i], "is_parent": nested[i] in header_list_faq}
            else:
                update(nested[i])

    def faq_list(nested):
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

    res = faq_list(nested_list_faq)
    with open(get_path('faq_list.pkl'), 'wb') as f:
        pickle.dump(res, f)