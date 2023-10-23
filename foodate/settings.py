import mimetypes
import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django_hosts import reverse
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.getenv('DEBUG', False) in ('1', 'True', 'true', 'T', 't')
SCHEME = os.getenv('SCHEME', 'https')
HOST = os.getenv('HOST', 'foodate.ru')
PARENT_HOST = HOST
VIRTUAL_MACHINE_IP = os.getenv('VM_IP')
ALLOWED_HOSTS = [HOST, f'm.{HOST}', f'book.{HOST}', VIRTUAL_MACHINE_IP]

# Application definition

INSTALLED_APPS = [
    'app.apps.AppConfig',
    'app_mobile.apps.AppMobileConfig',
    'book.apps.BookConfig',
    'users.apps.UsersConfig',
    'core.apps.CoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_hosts',
    'django_user_agents',
    'durationwidget',
    'django_quill',
    'hcaptcha',
    'rest_framework',
    'datetimewidget',
    'django_email_verification',
    'rest_framework.authtoken',
    'corsheaders',
    'social_django',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'core.middleware.RequestMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'app.urls'
ROOT_HOSTCONF = 'foodate.hosts'
DEFAULT_HOST = 'app'
HOST_SCHEME = f'{SCHEME}://'
SESSION_COOKIE_DOMAIN = f'.{HOST}'
CSRF_TRUSTED_ORIGINS = [f'{SCHEME}://*.{HOST}']

CORS_ALLOWED_ORIGINS = [
    f'{SCHEME}://{HOST}', f'{SCHEME}://m.{HOST}', f'{SCHEME}://book.{HOST}'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
            'builtins': [
                'django_hosts.templatetags.hosts_override',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodate.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'www/static'
STATICFILES_DIRS = (BASE_DIR / 'static',)
MEDIA_URL = 'uploads/'
MEDIA_ROOT = BASE_DIR / 'www/uploads'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = f'{SCHEME}://{HOST}/auth/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = f'{SCHEME}://{HOST}/auth/login'
AUTHENTICATION_BACKENDS = [
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.yandex.YandexOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'core.backends.EmailAuthBackend',
]
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Social auth

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'core.pipeline.social_user',
    'social_core.pipeline.user.get_username',
    'core.pipeline.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('VK_APP_ID')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('VK_API_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_YANDEX_OAUTH2_KEY = os.getenv('YANDEX_CLIENT_ID')
SOCIAL_AUTH_YANDEX_OAUTH2_SECRET = os.getenv('YANDEX_CLIENT_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_CLIENT_ID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# Email verification

def verified_callback(user):
    other_users_with_email = get_user_model().objects.filter(
        email=user.email,
        is_email_verified=True
    ).all()
    for user_ in other_users_with_email:
        user_.is_email_verified = False
        user_.save()
    user.is_email_verified = True


EMAIL_VERIFIED_CALLBACK = verified_callback
EMAIL_FROM_ADDRESS = EMAIL_HOST_USER
EMAIL_MAIL_SUBJECT = 'Подтверждение email'
EMAIL_MAIL_HTML = 'users/email_verification.html'
EMAIL_MAIL_PLAIN = 'users/email_verification.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60
EMAIL_MAIL_PAGE_TEMPLATE = 'users/email_verification_confirm.html'
EMAIL_PAGE_DOMAIN = f'{SCHEME}://{HOST}'
EMAIL_MULTI_USER = False

# hCaptcha

HCAPTCHA_SITEKEY = '4e5c5150-8547-4f93-bffb-94d4132c22b3'
HCAPTCHA_SECRET = '0xF77ec604cD33Bc25C866A82ca8402A74ea10D75e'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

if DEBUG:
    if HOST.endswith('.tk'):
        ALLOWED_HOSTS.append('localhost')
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    mimetypes.add_type('application/javascript', '.js')
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
