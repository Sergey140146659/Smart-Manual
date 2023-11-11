import json
import pandas as pd

from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.lemmatization import lemma_text

with open(get_path('articles.json'), 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open(get_path('faq.json'), 'r', encoding='utf-8') as f:
    faqs = json.load(f)

article = ' '.join(articles["article_lemma_text"]).split()
faq = ' '.join(faqs["faq_lemma_text"]).split()

data = {"вопрос": [], "класс": []}
for cnt in range(5, 6):
    for i in range(0, len(article), cnt):
        sentence = ' '.join(article[i: min(len(article), i + cnt)])
        data["вопрос"].append(sentence)
        data["класс"].append(1)
    for i in range(0, len(faq), cnt):
        sentence = ' '.join(faq[i: min(len(faq), i + cnt)])
        data["вопрос"].append(sentence)
        data["класс"].append(1)

with open("all_gpt4_texts.txt", "r") as file:
    text = file.read()

text = lemma_text(text).split()
for cnt in range(5, 6):
    for i in range(0, len(text), cnt):
        sentence = ' '.join(text[i: min(len(text), i + cnt)])
        data["вопрос"].append(sentence)
        data["класс"].append(0)

df = pd.DataFrame(data)
df.to_csv("questions_gpt4.csv")
