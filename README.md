# auto bot
[![License MIT](https://img.shields.io/badge/licence-MIT-green?style=flat-square)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black?style=flat-square)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C3.11-blue?style=flat-square)](#)
[![Telegram API](https://img.shields.io/badge/Telegram%20Bot%20API-6.9-blue?logo=telegram&style=flat-square)](https://core.telegram.org/bots/api)
[![Aiogram version](https://img.shields.io/badge/Aiogram-3.1.1-blue?style=flat-square)](https://aiogram.dev/)


# Описание
Телеграм бот для сохранения и поиска контактных данных автовладельцев-участников 
группы.

ID группы необходимо указать в переменной окружения `GROUP_ID` в `.env` файле.
Бот поддерживает только личную переписку с пользователем, обращения в группах 
отключены в `PrivateMiddleware`.

Бот должен быть добавлен в группу и иметь права администратора для проверки 
является ли пользователь ее участником. 

![Pic](https://github.com/andprov/auto_bot/blob/main/img/pic.png?raw=true "Pic")


# Установка
[Создать бота и получить](https://core.telegram.org/bots#how-do-i-create-a-bot) `BOT_TOKEN`

Возможно два сценария установки локально и в [Docker](https://docs.docker.com/engine/install/).

## Локальная установка
Для локальной установки необходимо наличие [PostgreSQL](https://www.postgresql.org/download/) 
в системе.

Клонировать репозиторий:
```shell
git clone <https or SSH URL>
```

Перейти в каталог проекта:
```shell
cd auto_bot
```

Создать файл `.env` с переменными окружения, со следующим содержанием:
```shell
# BOT
BOT_TOKEN=<bot_token>
GROUP_ID=<group_id>

# DB
DB_TYPE=postgresql
DB_CONNECTOR=psycopg
DB_HOST=localhost
DB_PORT=5432
POSTGRES_DB=bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Создать базу данных PostgreSQL с именем `bot`.

```shell
createdb -U postgres -h localhost -p 5432 bot
```

Создать и активировать виртуальное окружение:
```shell
python3 -m venv .venv
source .venv/bin/activate
```

Обновить pip:
```shell
pip install --upgrade pip
```

Установить зависимости:
```shell
pip install -r requirements.txt
```

Запустить приложение:
```shell
python -m app
```

## Установка в Docker на удаленный сервер
Дальнейшая инструкция предполагает, что удаленный сервер настроен на работу 
по SSH. На сервере установлен Docker. Зарегистрирован аккаунта на 
[hub.docker.com](https://hub.docker.com/)

Клонировать репозиторий:
```shell
git clone <https or SSH URL>
```

Перейти в каталог проекта:
```shell
cd auto_bot
```

Создать файл .env с переменными окружения, со следующим содержанием:
```shell
# BOT
BOT_TOKEN=<bot_token>
GROUP_ID=<group_id>

# DB
DB_TYPE=postgresql
DB_CONNECTOR=psycopg
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=bot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Docker images
BOT_IMAGE=<user_name/image_name>
DB_IMAGE=postgres:14
```

Подготовить docker images образ:
```shell
sudo docker build -t <username>/auto_bot .
```

Загрузить образ на Docker Hub:
```shell
sudo docker push <username>/auto_bot
```

Скопировать на удаленный сервер файлы `.env` `docker-compose.production.yml`
```shell
scp .env docker-compose.prod.yml <user@server-address>:/home/<user name>/
```

Подключиться к серверу:
```shell
ssh user@server-address
```

Выполнить сборку и запуск:
```shell
sudo docker compose -f docker-compose.prod.yml up -d
```
