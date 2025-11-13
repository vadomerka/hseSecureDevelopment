# Stage 1: Build stage - для установки зависимостей
FROM python:3.10-slim as builder

# Установка системных зависимостей для сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование только requirements файлов для оптимизации кэша
WORKDIR /build
COPY requirements.txt /build/

# Установка зависимостей в виртуальное окружение
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage - минимальный образ
FROM python:3.10-slim

# Установка только runtime зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Копирование виртуального окружения из builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создание non-root пользователя
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=/app

# Создание рабочей директории
WORKDIR /app

# Копирование только необходимых файлов приложения
COPY --chown=appuser:appuser . /app/task_app

# Создание директории для загруженных файлов с правильными правами
RUN mkdir -p /app/uploads && \
    chown -R appuser:appuser /app/uploads && \
    chmod 755 /app/uploads

# Переключение на non-root пользователя
USER appuser

# HEALTHCHECK для мониторинга состояния приложения
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Открытие порта
EXPOSE 8000

# Команда запуска приложения
CMD ["uvicorn", "task_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
