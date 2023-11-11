import g4f
import time

g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking

# openai.api_key = "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"
topics = [
    "Искусство и культура",
    "Здоровье и фитнес",
    "Путешествия и туризм",
    "Технологии и наука",
    "Мода и стиль",
    "Спорт и активный отдых",
    "Дом и семья",
    "Бизнес и финансы",
    "Еда и кулинария",
    "Образование и саморазвитие",
    "Развлечения и музыка",
    "Религия и духовность",
    "Природа и экология",
    "История и культурное наследие",
    "Психология и личностный рост",
    "Медиа и коммуникации",
    "Юмор и развлечения",
    "Животные и природа",
    "Дизайн и графика",
    "Фотография и видеосъемка",
    "Творчество и хобби",
    "Языки и лингвистика",
    "Политика и общество",
    "Межкультурные отношения и миграция",
    "Интерьер и декор",
    "Стиль жизни и личная организация",
    "Саморазвитие и мотивация",
    "Философия и этика",
    "Музыка и искусство звука",
    "Кино и телевидение",
    "Литература и поэзия",
    "Путешествия во времени и пространстве",
    "Гаджеты и электроника"
]

used_topic = ["Спасение вымирающих видов", "Музыкальный театр", "Путешествия во времени и пространстве",
              "Фотография и видеосъемка", "Огородничество", "Инновации и стартапы",
              "Роль семьи в формировании личности",
              "Как правильно выбирать чайную посуду и аксессуары для заваривания чая", "Религиозные традиции и ритуалы",
              "Искусство и культура", "Здоровье и фитнес",
              'Путешествия и туризм', "Технологии и наука", "Мода и стиль",
              "Спорт и активный отдых", "Дом и семья", "Бизнес и финансы", "Еда и кулинария",
              "Образование и саморазвитие", "Развлечения и музыка",
              "Религия и духовность", "Природа и экология"
              ]

for i in range(len(topics)):
    topic = topics[i]
    if topic in used_topic:
        continue
    prompt = f'составь небольшой текст на тему "{topic}"'
    go = 1

    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": prompt}],
        )
        response = str(response)
        with open('texts_gpt4.txt', 'a') as file:
            file.write(response)
        print(f'{topic}:\n{response}')
        used_topic.append(topic)
    except:
        new_prompt = f'составь небольшой текст по теме "{topic}"'
        time.sleep(30)
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": prompt}],
            )
            response = str(response)
            with open('texts_gpt4.txt', 'a') as file:
                file.write(response)
            print(f'{topic}:\n{response}')
            used_topic.append(topic)
        except:
            continue

print("used:", used_topic)
unused = []
for i in topics:
    if i not in used_topic:
        unused.append(i)
print("unused:", unused)
