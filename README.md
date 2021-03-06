Данный сервис выполняет заявку на провоз лыж.

# Установка

Склонируйте данный репозиторий и установите зависимости из [requirements/dev.txt](requirements/dev.txt).

# Запуск

Чтобы запустить сервис, выполните команду в консоли:

`uvicorn ski.main:app --reload`

Также возможно запустить серсив из Docker-образа. Чтобы собрать образ и запустить сервис, 
выполните команду:

`docker build -t <image-name> .`

`docker run -d -p 8000:8000 -v <folder-with-configs>/configs.yml:/usr/app/configs.yml --name ski <image-name>`

где `<folder-with-configs>` - путь до папки, в которой лежит файл `configs.yml` с конфигами сервиса. 
Пример конфигурационного файла можно посмотреть в файле [configs.example.yml](configs.example.yml).

Сервис будет доступен по адресу `0.0.0.0:8000`.

# Начало работы

Сервис предоставляет единственный эндпойнт - `/`. На этот эндпойнт необходимо выполнять
`GET`-запрос с параметрами `number` и `passengerId`. Например:

`http://0.0.0.0:8000/?passengerId=ivanov&number=AAAAAA`

Оба параметра обязательные.

# Документация

Документация доступна по эндпойнтам `/docs` и `/redoc`.

