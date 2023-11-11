import re
import requests
from bs4 import BeautifulSoup
import json
from ml.request_processing.lemmatization import lemma_text
from ml.preprocessing_data.Articles_path import get_path


def law44_db_create():
    """
    Функция law44_db_create() создает базу данных фз-44 в виде JSON-файла laws44.json.
    Функция создает словарь laws, содержащий следующие ключи:

    law_info: список словарей, каждый из которых содержит информацию о статье.
    law_name: список названий статей.
    law_text: список текстов статей.
    law_lemma_text: список лемматизированных текстов статей.
    law_combined_text: список текстов статей, объединенных с лемматизированными версиями.
    law_link: список ссылок на статьи.
    """
    laws = {
        "law_info": [

        ],
        "law_name": [

        ],
        "law_text": [

        ],
        "law_lemma_text": [

        ],
        "law_combined_text": [

        ],
        "law_link": [

        ]
    }

    def get_text(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tag = soup.find('div', {'class': 'block'})
        div_text = div_tag.get_text()
        while "\n\n" in div_text:
            div_text = div_text.replace("\n\n", "\n")
        return div_text

    def get_header(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        header = soup.find('h1').text.strip()
        return header

    page = requests.get("https://base.garant.ru/70353464/")
    soup = BeautifulSoup(page.content, 'html.parser')
    ul_tag = soup.find('ul', {'id': 'ul_num1'})
    links = ul_tag.find_all('a')
    texts = ul_tag.find_all('h2')

    name_link = []
    for i in range(len(links)):
        link = f"https://base.garant.ru{links[i].get('href')}"
        header = get_header(link)
        if ("Статья" in header) and ("утратила силу" not in header) and ("утратил силу" not in header):
            name_link.append((header, link))

    for name, link in name_link:
        law_name = name
        law_text = get_text(link)
        law_text = law_text.replace(" ", " ")
        law_lemma_text = lemma_text(law_text)
        law_lemma_text = re.sub(r'\b\w\b', '', law_lemma_text)
        while "  " in law_lemma_text:
            law_lemma_text = law_lemma_text.replace("  ", " ")
        law_combined_text = law_text + ' ' + law_lemma_text
        law_info = {
            "law_name": law_name,
            "law_text": law_text,
            "law_lemma_text": law_lemma_text,
            "law_combined_text": law_combined_text,
            "law_link": link
        }
        laws["law_info"].append(law_info)
        for column, content in law_info.items():
            laws[column].append(content)

    with open(get_path("laws44.json"), 'w', encoding='utf-8') as f:
        json.dump(laws, f)
