# Django settings for autodata project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/changeformrepro',
    }
}

SECRET_KEY = 'mq%31q+sjj^)m^tvy(klwqw6ksv7du2yzdf9yn78iga*r%8w^t-changeformrepro'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.messages',
    'changeformrepro',
)

STATIC_URL = '/static/'

ROOT_URLCONF = 'changeformrepro.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
