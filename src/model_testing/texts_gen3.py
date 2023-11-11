import g4f, time

g4f.logging = True  # enable logging
g4f.check_version = False  # Disable automatic version checking

# openai.api_key = "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"
topics = ['История науки и технологий']

used_topic = ["Спасение вымирающих видов", "Музыкальный театр", "Путешествия во времени и пространстве",
              "Фотография и видеосъемка", "Огородничество", "Инновации и стартапы",
              "Роль семьи в формировании личности",
              "Как правильно выбирать чайную посуду и аксессуары для заваривания чая", "Религиозные традиции и ритуалы",
              "Искусство и культура", "Здоровье и фитнес",
              'Путешествия и туризм', "Технологии и наука", "Мода и стиль",
              "Природа и экология", "Религия и духовность", "Развлечения и музыка", "Образование и саморазвитие",
              "Еда и кулинария", "Бизнес и финансы",
              "Дом и семья", "Спорт и активный отдых", "Мода и красота", "Жизненный опыт и советы",
              "Психология отношений и любовь",
              "Спиритуализм и мистика", "Кулинарные рецепты и диеты", "Автомобили и транспорт",
              "Спорт и фитнес-технологии", "Уход за здоровьем и медицина",
              "Отдых на природе и кемпинг", "Игры и развлечения для детей", "Религиозные традиции и культуры",
              "Ремонт и строительство"
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
