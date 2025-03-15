# Dockerfile для Streamlit (frontend)

# Базовый образ с Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./frontend.py /app/

# Устанавливаем зависимости
RUN pip install streamlit requests

# Открываем порт для Streamlit
EXPOSE 8501

# Команда для запуска приложения
CMD ["streamlit", "run", "frontend.py"]