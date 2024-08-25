from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xhigpsi^68!yw#h@p3!d1=_(bt_%*j87i&+sogvhik4osu=^lc'  # Consider using environment variables for this in production

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Define allowed hosts. For production, specify your domain or IP.
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Replace with your domain names or IP addresses for security

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listings',  # Ensure your app is listed here
    'corsheaders',  # Add CORS headers
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rent_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Directory for project-wide templates
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

WSGI_APPLICATION = 'rent_site.wsgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '310524ptm_rubila341_final',
        'USER': 'ich1',
        'PASSWORD': 'ich1_password_ilovedbs',
        'HOST': 'mysql.itcareerhub.de',
        'PORT': '3306',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'  # Ensure the leading slash is present
STATICFILES_DIRS = [BASE_DIR / 'static']  # Directory for project-wide static files

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirect URLs
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only; use CORS_ALLOWED_ORIGINS in production
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

# Cookie settings
SESSION_COOKIE_SAMESITE = 'None'  # Adjust based on your needs
SESSION_COOKIE_SECURE = True  # Set to True if you're using HTTPS
CSRF_COOKIE_SAMESITE = 'None'  # Adjust as needed
CSRF_COOKIE_SECURE = True  # Set to True if you're using HTTPS
