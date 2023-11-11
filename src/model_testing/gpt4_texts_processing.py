str_to_replace = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–"

stopword = ['и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но',
            'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня',
            'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни',
            'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя',
            'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем',
            'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто',
            'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем',
            'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два',
            'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них',
            'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда',
            'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между', 'для',
            'быть', 'если', 'или', 'который', 'это', 'при', 'тот', 'только', 'как', 'так', 'он', 'child', 'toc', 'наш',
            'также', 'свой', 'мы', 'ваш', 'однако', 'конечно']
import pymorphy3

morph = pymorphy3.MorphAnalyzer()


def get_normal_form(word):
    return morph.parse(word)[0].normal_form


def lemma_text(text):
    text = text.lower()
    for i in str_to_replace:
        text = text.replace(i, ' ')
    text = text.split()
    for i in range(len(text)):
        if text[i] in stopword or len(text[i]) <= 2:
            text[i] = ""
        else:
            text[i] = get_normal_form(text[i])
            if text[i] in stopword or len(text[i]) <= 2:
                text[i] = ""
    text = ' '.join(text)
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


text_gpt4 = read_file("texts_gpt4.txt")
text_gpt4_1 = read_file("texts_gpt4_1.txt")
text_gpt4_2 = read_file("texts_gpt4_2.txt")
text_gpt4_3 = read_file("texts_gpt4_3.txt")
processing_text_gpt4 = lemma_text(text_gpt4)
processing_text_gpt4_1 = lemma_text(text_gpt4_1)
processing_text_gpt4_2 = lemma_text(text_gpt4_2)
processing_text_gpt4_3 = lemma_text(text_gpt4_3)
with open('all_gpt4_texts', 'a') as file:
    file.write(processing_text_gpt4)

with open('all_gpt4_texts', 'a') as file:
    file.write(' ' + processing_text_gpt4_1)

with open('all_gpt4_texts', 'a') as file:
    file.write(' ' + processing_text_gpt4_2)

with open('all_gpt4_texts', 'a') as file:
    file.write(' ' + processing_text_gpt4_3)