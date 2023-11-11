import language_tool_python
from spellchecker import SpellChecker

tool = language_tool_python.LanguageTool('ru-RU')
spell_ru = SpellChecker(language='ru')


def correct(word):
    '''
    Если слово может быть исправлено с помощью spellchecker:
    -Используя spellchecker, функция получает список возможных исправлений для данного слова.
    -Если список возможных исправлений не пустой, функция возвращает первое исправление из списка.

    Если слово не может быть исправлено с помощью spellchecker:
    -Используя language_tool_python, функция проверяет слово на наличие ошибок.
    -Если ошибки обнаружены и есть предложенные замены:
    -Функция возвращает первую замену из списка предложенных замен.
    -Если ошибки обнаружены, но нет предложенных замен, функция возвращает исходное слово без изменений.
    '''
    corrected_word = spell_ru.candidates(word)
    if corrected_word is None:
        matches = tool.check(word)
        if len(matches) == 0:
            return word
        if len(matches[0].replacements) == 0:
            return word
        if len(matches[0].replacements[0]) == 0:
            return word
        return matches[0].replacements[0]
    else:
        return next(iter(corrected_word))
