# About TBOT_WB
Телеграм бот для wildberies, умеет:
- предоставлять информацию о товаре по артикулу
- делать рассылку пользователю согласно его подписок на информацию о товарах
- отменять подписку
- предоставлять последние пять подписок из базы данных

# Stack
- Python 3.10
- aiogram==3.4.1
- python-dotenv==1.0.1
- SQLAlchemy==2.0.28
- psycopg2-binary==2.9.9
- APScheduler==3.10.4
- requests==2.31.0
и т.д. -> requirements.txt

# To start 

1. стяни ветку мастер - pull master from github
2. сделай свои файлы docker и docker-compose со своими настройками переменных ENV на основе файлов sample 
3. запусти docker-compose up --build

# To develope

1. стяни ветку мастер - pull master from github
2. не забудь установить зависимости pip install -r requirements.txt
3. создай базу postges
4. создай свой файл .env со своими настройками на основе sample файла
5. в функции load_config() нужно везде прокинуть путь к файлу .env
6. запусти файл main.py

# To do

1. Сделать админку
2. Сделать тесты
3. Сделать EN версию тестов и подключить
4. Добавить загрузку картинки товара
