import json
from ml.preprocessing_data.Articles_path import get_path
from ml.request_processing.gramma_checker import correct

str_to_replace = "!«»\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r\x0b\x0c\x0a\xa0–0123456789"
replace_dict = str.maketrans(str_to_replace, ' ' * len(str_to_replace))


def remove_non_letters(text):
    '''
    -Заменяет все символы, которые не являются буквами, на пробелы, используя словарь "replace_dict".
    -Приводит все символы к нижнему регистру.
    -Удаляет пробелы в начале и конце строки.
    -Удаляет повторяющиеся пробелы внутри строки.
    '''
    text = text.translate(replace_dict)
    text = text.lower()
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.count += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count

    def starts_with(self, prefix):
        node = self.root
        words = []
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        self._dfs(node, prefix, words)
        return sorted(words, key=lambda x: x[1], reverse=True)

    def _dfs(self, node, prefix, words):
        if node.count > 0:
            words.append((prefix, node.count))
        for char in node.children:
            self._dfs(node.children[char], prefix + char, words)


def remove_non_letters(text):
    text = text.translate(replace_dict)
    text = text.lower()
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text


article_trie = Trie()  # префиксное дерево, в котором содержатся все слова из конспектов

# загрузка всех слов в бор
subs = ["subject1.json", "subject2.json", "subject3.json", "subject4.json", "subject5.json"]

for sub in subs:
    with open(get_path(sub), 'r') as file:
        data = json.load(file)
        # combined_text_of_sections
    for section in data["combined_text_of_sections"]:
        for word in section.split(' '):
            article_trie.insert(word)


def check_word(word):
    '''
    Проверяет, является ли длина слова меньше 3 символов. Если это так, то возвращает пустую строку.
    Ищет слово в префиксном дереве "article_trie". Если слово найдено, возвращает его.
    Если слово не найдено, проверяет все возможные префиксы слова (от начала до последних трех символов) и ищет их в "article_trie". Если находит первый найденный префикс, возвращает его.
    Если ни один из префиксов не найден в "article_trie", вызывает функцию "correct(word)", которая исправляет опечатки в слове и возвращает исправленное слово.
    '''
    if len(word) < 3:
        return ''
    word = word[0: min(25, len(word))]
    if article_trie.search(word) > 0:
        return word
    for i in range(0, 3):
        if len(word) - i <= 2:
            break
        pref = article_trie.starts_with(word[0: len(word) - i])
        if len(pref) != 0:
            return pref[0][0]
    return correct(word)
