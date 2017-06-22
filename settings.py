import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if os.environ.get('DATABASE_URL'):
    import dj_database_url

    db_from_env = dj_database_url.config()
    DATABASES['default'] = dj_database_url.config()

INSTALLED_APPS = (
    'db',
)

SECRET_KEY = 'And Then There Were None'

DEBUG = False
if os.environ.get('DEBUG'):
    DEBUG = True
