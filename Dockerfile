# Используйте официальный базовый образ Python
FROM python:3.11.6

# Установите рабочий каталог в контейнере
WORKDIR /code

COPY . .

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

## Установка Nginx
#RUN apt-get update && \
#    apt-get install -y nginx && \
#    rm -rf /var/lib/apt/lists/*
#
## Копирование конфигурации Nginx
#COPY ./nginx-conf/default.conf /etc/nginx/conf.d/default.conf

# Команда для запуска приложения
CMD ["python", "-u", "main.py"]