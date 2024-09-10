# Выявление значимых общественно-политических и экономических событий на курсовую стоимость валюты на основе семантического анализа

## Цели проекта

- Исследование связи между общественно-политическими и экономическими событиями и колебаниями валютных курсов с помощью методов машинного обучения.
## Установка

1. Клонируйте репозиторий:

   ```sh
   git clone https://gitlab.mai.ru/cifra1/data-collection/async_parser_tass.git

2. Установите зависимости

    ```sh
   pip install -r requirements.txt

## Запуск программы

1. Запуск PostgreSQL
    ###### Убедитесь, что PostgreSQL запущен и доступен. Вы можете использовать Docker для быстрого запуска экземпляра PostgreSQL:
    ```sh
   docker run --name postgres -e POSTGRES_PASSWORD=yourpassword -d -p 5432:5432 postgres
2. Выполнение миграций Alembic
    ###### Для применения миграций и создания необходимых таблиц в базе данных, выполните следующую команду:
    ```sh
   alembic upgrade head
   
3. Запустите приложение
    ```sh
   python main.py
   
## Конфигурация
- Перед запуском приложения убедитесь, что у вас правильно настроены параметры подключения к базе данных в файле конфигурации. Пример строки подключения к базе данных:
   ```sh
  sqlalchemy.url = postgresql+asyncpg://<DB_USER>:<DB_PASSWORD>@<DB_HOST>/<DB_NAME>

## Использование

- Приложение будет запущено и доступно по адресу http://localhost:8000. Вы можете взаимодействовать с API через этот URL.

## Дополнительная информация
- Для получения дополнительной информации и настроек обратитесь к документации в репозитории или свяжитесь с автором проекта.#   D i g i t - b a c k e n d  
 