import os

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    _ = get_wsgi_application()
