# Инструкция по развертыванию на Render

## 1. Создание базы данных
Зайдите на Render.com и нажмите кнопку "+ New". Выберите "Postgres". Заполните имя (например, srs7-db), выберите регион (Oregon) и бесплатный тариф (Free). Нажмите "Create Database". Дождитесь, пока статус станет "Available". Скопируйте ссылку "External Database URL" (она понадобится дальше).

## 2. Создание Web Service
Нажмите снова "+ New" и выберите "Web Service". Подключите ваш GitHub и выберите репозиторий с проектом. Заполните поля:
- Name: любое имя (например, srs7).
- Region: Oregon (как у базы данных).
- Root Directory: оставьте пустым если manage.py лежит в корне.
- Build Command: bash build.sh
- Start Command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
- Instance Type: Free.

## 3. Переменные окружения
В разделе "Environment" добавьте переменные:
- DATABASE_URL: вставьте ссылку из шага 1.
- DJANGO_SECRET_KEY: нажмите "Generate".
- DJANGO_DEBUG: False.
- DJANGO_ALLOWED_HOSTS: адрес вашего сайта (например, srs7.onrender.com).
- DJANGO_CSRF_TRUSTED_ORIGINS: адрес вашего сайта с https (например, https://srs7.onrender.com).

## 4. Запуск и проверка
Нажмите "Create Web Service". Дождитесь, пока статус станет "Live". Откройте сайт по ссылке. Войдите в админку (/admin/) под созданным пользователем. Проверьте работу API (например, /api/course-proposals/).

## 5. Частые проблемы
- Ошибка "DisallowedHost": проверьте, что в DJANGO_ALLOWED_HOSTS указан ваш домен.
- Ошибка "build.sh not found": проверьте Root Directory (должна быть папка с manage.py).
- Ошибка 500: проверьте логи на Render (раздел Logs). Чаще всего это связано с миграциями или переменными окружения.