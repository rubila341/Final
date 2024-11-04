from pathlib import Path

# Построение путей внутри проекта, например: BASE_DIR / 'subdir'.
# Erstellung von Pfaden innerhalb des Projekts, z. B. BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-xhigpsi^68!yw#h@p3!d1=_(bt_%*j87i&+sogvhik4osu=^lc'


DEBUG = True  # Установите False в продакшене !!!/ In der Produktion auf False setzen

# Определите разрешённые хосты. Указать домен или IP на продакшене !!!.
# Definieren Sie die erlaubten Hosts. Geben Sie die Domäne oder IP für die Produktion an.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Определение установленных приложений.
# Definition der installierten Anwendungen.
INSTALLED_APPS = [
    'jet',  # Jet должен быть в начале для переопределения админки ( так как установил не стандартную админку / Jet sollte am Anfang sein, um das Admin-Panel zu überschreiben
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listings',
    'corsheaders',  # Добавление заголовков CORS для разрешения междоменных запросов/ Hinzufügen von CORS-Headern
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Добавление CORS middleware / Hinzufügen von CORS-Middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной конфигурационный файл URL
# Haupt-URL-Konfigurationsdatei
ROOT_URLCONF = 'rent_site.urls'

# Шаблоны
# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Каталог для шаблонов проекта / Verzeichnis für projektweite Templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Приложение WSGI делал в частности для настройки докера
# WSGI-Anwendung
WSGI_APPLICATION = 'rent_site.wsgi.application'

# Конфигурация базы данных
# Datenbankkonfiguration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '310524ptm_rubila341_final',  # Название базы данных / Name der Datenbank
        'USER': 'ich1',  # Пользователь базы данных / Datenbank-Benutzer
        'PASSWORD': 'ich1_password_ilovedbs',  # Пароль базы данных / Datenbank-Passwort
        'HOST': 'mysql.itcareerhub.de',  # Хост базы данных / Datenbank-Host
        'PORT': '3306',  # Порт базы данных / Datenbank-Port
    }
}

# Валидация паролей
# Passwortvalidierung
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'  # Язык по умолчанию / Standardsprache
TIME_ZONE = 'UTC'  # Часовой пояс / Zeitzone
USE_I18N = True  # Включить интернационализацию / Internationalisierung aktivieren
USE_TZ = True  # Включить поддержку часовых поясов / Zeitzonenunterstützung aktivieren

# Статические файлы (CSS, JavaScript, Изображения)
# Statische Dateien (CSS, JavaScript, Bilder)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Каталог для статических файлов / Verzeichnis für statische Dateien während der Entwicklung
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Для продакшена  статика/ Für Produktion

# Медиафайлы (Загруженные пользователями файлы)
# Mediendateien (vom Benutzer hochgeladene Dateien)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки для установки по умолчанию для первичных ключей
# Standardmäßige Primärschlüssel-Einstellung
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL перенаправления после входа и выхода
# Umleitungs-URLs nach dem Ein- und Ausloggen
LOGIN_REDIRECT_URL = '/profile/'  # когда проходит логинрование, сделал проброс на профиль/ Umleitung nach erfolgreichem Login
LOGOUT_REDIRECT_URL = '/'  # когда происходит логаут сделал перенаправление на главную / Umleitung nach dem Logout

# Настройки CORS (разрешение запросов с разных доменов)
# CORS-Einstellungen (Erlauben von Anfragen von verschiedenen Domänen)
CORS_ALLOW_ALL_ORIGINS = True  # Разрешено для разработки

# Настройки cookie. делал попытки настройки https://
# Cookie-Einstellungen
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True  # Установите True, если используете HTTPS / Auf True setzen, wenn HTTPS verwendet wird
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True  # Установите True, если используете HTTPS / Auf True setzen, wenn HTTPS verwendet wird

# URL для входа ( прописываю через какую ссылку проходит логирование)
# Login-URL-Konfiguration
LOGIN_URL = '/login/'

# Конфигурация Django Jet (дополнительная настройка)
# Django Jet-Konfiguration (optionale Anpassung)
JET_THEMES = [
    {
        'theme': 'default',  # Настройка тем (поставил стандартную) / Themen anpassen
        'color': '#47bac1',
    },
]

# Дополнительные настройки безопасности для продакшена (тажа настройка https
# Zusätzliche Sicherheitseinstellungen für die Produktion (empfohlen)
if not DEBUG:
    SESSION_COOKIE_SECURE = True  # Обеспечение безопасности куки сессий / Sitzungs-Cookies sichern
    CSRF_COOKIE_SECURE = True  # Обеспечение безопасности CSRF куки / CSRF-Cookies sichern
    SECURE_SSL_REDIRECT = True  # Перенаправление на HTTPS / Umleitung auf HTTPS
