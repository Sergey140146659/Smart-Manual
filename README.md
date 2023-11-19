# Smart Search
 
## Инструкция
Для запуска проекта необходимо создать виртуальное окружение командой `python -m venv venv` и активировать его. Команда `venv\Scripts\activate.bat` - для Windows; `source venv/bin/activate` - для Linux и MacOS.

Затем необходимо установить зависимости командой `pip install -r requirements.txt`.

Скачать архив(https://drive.google.com/file/d/1TZVrXMABtPdCswNto_45OH1uV3cH7V3t/view?usp=sharing) и распаковать его в папку `src/classification/bert_model`

Затем необходимо перейти в папку `src` командой `cd src` и запустить команду `uvicorn main:app --reload` для запуска сервера `uvicorn`.

После этого можно зайти в браузере по адресу `http://localhost:8000/pages/search` для доступa к приложению или по `http://localhost:8000/pages/admin_db_upload` для доступа к админке.
