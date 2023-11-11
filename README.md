# Smart Search
 
## Инструкция
Для локального тестирования необходимо создать виртуальное окружение командой `python -m venv venv` и активировать его. Команда `venv\Scripts\activate.bat` - для Windows; `source venv/bin/activate` - для Linux и MacOS.

Затем необходимо перейти в папку с нужным уроком и установить зависимости командой `pip install -r requirements.txt`.

Затем необходимо перейти в папку `src` командой `cd src` и запустить команду `uvicorn main:app --reload` для запуска сервера `uvicorn`. 

Обновление базы данных `alembic upgrade head`.

После этого можно зайти в браузере по адресу `http://localhost:8000/docs` для просмотра доступных эндпоинтов.
