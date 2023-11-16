import json

import pandas as pd

from ml.preprocessing_data.Articles_path import get_path

subs = [
    "subject1.json",
    "subject2.json",
    "subject3.json",
    "subject4.json"
]
all_text = ''

for sub in subs:
    with open(get_path(sub), 'r') as file:
        data = json.load(file)

    for j in data["combined_text_of_sections"]:
        all_text += " "
        all_text += j

all_text = all_text.split()
sentences = [all_text[i:i + 5] for i in range(0, len(all_text), 5)]

data = {
    "вопрос": [],
    "класс": []
}
for i in sentences:
    data["вопрос"].append(' '.join(i))
    data["класс"].append(1)

df_add = pd.DataFrame(data)
df_orig = pd.read_csv("questions_gpt4.csv")
df_new = pd.concat([df_orig, df_add])
df_new.to_csv("dataset.csv",index = False)
