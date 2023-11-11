from ml.request_processing.abbers_errors import check_word
from ml.request_processing.lemmatization import lemma_text

str_to_replace = "!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–"
replace_dict = str.maketrans(str_to_replace, ' ' * len(str_to_replace))


def request_processing(request):
    '''
    обрабатывает текст запроса, исправляет опечатки в словах,
    удаляет лишние слова, лемматизирует оставшиеся слова и возвращает лемматизированный запрос
    '''
    request = request.lower()
    for i in str_to_replace:
        request = request.replace(i, ' ')
    while '  ' in request:
        request = request.replace('  ', ' ')
    words = request.split()
    words = words[0: min(50, len(words))]
    words = [check_word(i) for i in words]
    text = ' '.join(words)
    text = lemma_text(text)
    return text
