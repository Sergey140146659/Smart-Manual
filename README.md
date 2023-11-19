# Smart Search
 
## Инструкция
Для запуска проекта необходимо создать виртуальное окружение командой `python -m venv venv` и активировать его. Команда `venv\Scripts\activate.bat` - для Windows; `source venv/bin/activate` - для Linux и MacOS.

Затем необходимо установить зависимости командой `pip install -r requirements.txt`.

Затем необходимо перейти в папку `src` командой `cd src` и запустить команду `uvicorn main:app --reload` для запуска сервера `uvicorn`.

После этого можно зайти в браузере по адресу `http://localhost:8000/search` для доступa к приложению или по `http://localhost:8000/admin` для доступа к админке.
