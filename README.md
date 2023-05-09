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
При помощи curl
1. Пример:
```bash
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "" 127.0.0.1:8000/api/users/register/
```
```bash
{"status": 1, "error": "No parameter: username"}
```

2. Пример:
```bash
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "username=Maria" 127.0.0.1:8000/api/users/register/
```
```bash
{"status": 0, "message": "User Maria is currently registered"}
```

3. Пример:
```bash
curl 127.0.0.1:8000/api/users/1/
```
```bash
{"user": {"id": 1, "username": "Maria"}}
```

4. Пример:
```bash
curl 127.0.0.1:8000/api/users/1/requests/
```
```bash
{"requests": [{"id": 1, "sender_id": 1, "reciever_id": 2, "is_confirmed": true}, {"id": 2, "sender_id": 1, "reciever_id": 3, "is_confirmed": false}, {"id": 5, "sender_id": 4, "reciever_id": 1, "is_confirmed": true}]}
```

Узнать больше: [документация](https://github.com/AlSerP/vk_friends_api/tree/master/docs) 