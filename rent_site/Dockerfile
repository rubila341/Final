# Используем базовый образ
FROM python:3.9-slim

# Устанавливаем необходимые пакеты для сборки
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    pkg-config \
    libmysqlclient-dev && \
    apt-get clean

# Устанавливаем рабочий каталог
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочий каталог
COPY . /app/

# Устанавливаем команду для запуска приложения
CMD ["gunicorn", "rent_site.wsgi:application", "--bind", "0.0.0.0:8000"]
