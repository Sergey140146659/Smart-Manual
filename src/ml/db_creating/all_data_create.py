from ml.db_creating.article_list_creating import article_list_creating
from ml.db_creating.articles_db_create import article_db_create
from ml.db_creating.faq_db_create import faq_db_create
from ml.db_creating.faq_list_creating import faq_list_creating
from ml.db_creating.law223_db_create import law223_db_create
from ml.db_creating.law44_db_create import law44_db_create

"""
Этот Python-скрипт создает базу данных с нуля для законов, статей и часто задаваемых вопросов (FAQ).

Сначала выполняется два бесконечных цикла while True,
каждый из которых пытается создать базу данных для закона 223 и закона 44 соответственно.
Если возникает исключение, код продолжает выполнение цикла, пытаясь снова создать базу данных.

Затем следуют вызовы функций article_db_create(), faq_db_create(), article_list_creating() и faq_list_creating(),
которые создают базу данных для статей и FAQ, а также выполняют дополнительные действия,
связанные с созданием списков статей и FAQ.

В результате выполнения этого скрипта будет создана полная база данных с нуля,
включая законы, статьи и часто задаваемые вопросы.

Важно отметить, что при выполнении этого Python-скрипта будет произведено полное удаление базы данных с вопросами.
"""

while True:
    try:
        law223_db_create()
        break
    except Exception as e:
        continue

while True:
    try:
        law44_db_create()
        break
    except Exception as e:
        continue

article_db_create()
faq_db_create()
article_list_creating()
faq_list_creating()
