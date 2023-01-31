# Групповой проект - API_YAMDB

**Разработчики:**
- [Елистратова Полина (тимлид, разработка ресурсов Auth и Users)](https://github.com/TIoJIuHa)
- [Саидов Ратмир (разработка ресурсов Categories, Genres и Titles)](https://github.com/RatmirSaidov)
- [Шапченко Дмитрий (разработка ресурсов Review и Comments)](https://github.com/dltt1)

### Стек технологий:

<div>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green"/>
  <img src="https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white"/>
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white"/>
  <img src="https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white"/>
</div>


### Описание

Проект выполнен в учебных целяx для курса Яндекс.Практикума. **YaMDb** собирает отзывы пользователей на произведения. Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число). Пользователи могут оставлять комментарии к отзывам.

[Полная документация по API (redoc.yaml)](api_yamdb\static\redoc.yaml)

#### Алгоритм регистрации пользователей

  1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
  2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
  3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
  4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

#### Пользовательские роли

  - **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
  - **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
  - **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
  - **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
  - **Суперюзер Django** — обладет правами администратора (`admin`)

#### Запуск проекта в контейнерах

Для начала нужно клонировать репозиторий и перейти в корневую папку проекта:
```
git clone <project_url>
cd infra_sp2
```

Затем нужно перейти в папку `infra/` и создать в ней файл `.env` с  переменными окружения, необходимыми для работы приложения.
```
cd infra/
```

*Пример содержимого файла:*
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Далее следует запустить docker-compose. В фоновом режиме будут созданы и запущены необходимые для работы приложения контейнеры (`db`, `web`, `nginx`): 
```
docker-compose up -d
```

Затем нужно внутри контейнера `web` создать и выполнить миграции, создать суперпользователя и собрать статику:
```
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations reviews
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
После этого проект станет доступен по адресу http://localhost/. 

#### Заполнение базы данных

Необходимо перейти по адресу http://localhost/admin/, авторизоваться и внести записи в базу данных через админку.

Резервную копию базы данных можно создать командой
```
docker-compose exec infra-web python manage.py dumpdata > fixtures.json 
```
