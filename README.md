# Тестовое задание (Сервис-друзей)

## Запуск проекта

1. Клонирование репозитория:
```bash
      git clone https://github.com/AlSerP/vk_friends_api .
```

2. Создание и активация виртуального окружения:
```bash
      python -m venv django_venv
      venv\Script\activate
```

3. Установка Django:
```bash
    (django_venv)  pip install -r requirements.txt
```

4. Применение миграций:
```bash
    (django_venv)  python manage.py migrate
```

5. Запуск сервера:
```bash
    (django_venv)  python manage.py runserver
```

## Пример использования API

Запрос:
```bash
    curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "" 127.0.0.1:8000/api/users/register/
```
Ответ:
```bash
    {"status": 1, "error": "No parameter: username"}
```
