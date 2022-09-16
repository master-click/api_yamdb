# Проект «API для Yatube»

## Автор: Макарьев Никита

***
Задача проекта заключается в приобретении практических навыков работы с **Django REST framework**. Проект **api_yatube** содержит приложение posts с описанием моделей **Yatube**. В данном проекте реализован API для всех моделей приложения.

***

Для работы с API проекта необходимо пройти процедуру аутентификации. Процесс аутентификации осуществляется посредством использования JWT-токена.
Исчерпывающий перечень запросов доступен по адресу http://127.0.0.1:8000/redoc/.

***

Разворачивание проекта:

Клонировать репозиторий и перейти в его папку в командной строке:

```bash
git clone https://github.com/NikitaMackariev/api_final_yatube.git
```

```bash 
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```bash 
python3 -m venv venv
```

Для *nix-систем:

```bash 
. venv/bin/activate
```

Для windows-систем:

```bash 
. venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```bash 
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```bash 
cd yatube_api
python manage.py makemigrations
python manage.py migrate
```

Запустить проект:

```bash 
python manage.py runserver
```

Создать суперпользователя django:

```bash 
python manage.py createsuperuser
```

Придумайте логин (например, admin):
```bash
Username (leave blank to use 'user'):
```

Укажите почту:
```bash
Email address:
```

Придумайте пароль:
```bash
Password:
```

Повторите пароль:
```bash
Password (again):
```

Суперпользователь успешно создан:
```bash
Superuser created successfully.
```

Сам проект и админ-панель доступны по адресам:

```
http://127.0.0.1:8000
http://127.0.0.1:8000/admin
```

***

Некоторые примеры запросов к API.

**Получение списка записей:**

эндпойнт:

```
/api/v1/posts/
```

разрешённые HTTP-методы:

```
GET
```

в ответе:

```python
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "pub_date": date,
    "image": image,
    "group": 0
  }
]
```

**Получение сообщества:**

эндпойнт:

```
/api/v1/groups/{id}/
```

разрешённые HTTP-методы:

```
GET
```

в ответе:

```python
[
  {
    "title": "string",
  }
]
```

**Создание комментария**

эндпойнт:
```
/api/v1/posts/{post_id}/comments/
```

http-метод:
```
POST
```

Payload:
```python
{
  "post": 0,
  "text": "string"
}
```

Варианты ответов:
* комментарий создан: статус 201 
```python
{
  "id": 1,
  "author": "string",
  "post": 1,
  "text": "string",
  "created": date
}
```

* запрос отклонен: статус 400 - отсутствует обязательное поле в теле запроса
```python
{
  "post": [
    "Обязательное поле."
  ]
}
```

* запрос отклонен: статус 401 - запрос от имени анонимного пользователя
```python
{
  "detail": "Учетные данные не были предоставлены."
}
```

* запрос отклонен: статус 404 - попытка добавить комментарий к несуществующей публикации
```python
{
  "detail": "Страница не найдена."
}
```
