# nvim_django_diploma
Дипломная работа по джанго выполняется в редакторе nvim

Клонируем репозиторий
git clone git@github.com:sejeenn/nvim_django_diploma.git

Переходим в директорию nvim_django_diploma

Создаем виртуальное окружение 
python -m venv .venv

устанавливаем зависимости: pip istall -r requirements.txt
устанавливаем файлы из архива: pip install diploma-frontend-0.6.tar.gz

Создаем django-проект: django-admin startproject backend (ну или другое имя проекту даем)
Переходим в директорию проекта cd backend/backend/
Добавляем в файл settings.py строчку frontend:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'frontend',
]

Добавляем в файл urls.py строчки include и path('', include('frontend.urls')):
from django.contrib import admin
from django.urls import include, path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]

Выполняем миграции python manage.py migrate
Запускаем тестовый сервер python manage.py runserver

Вроде бы ничего не упустил...
