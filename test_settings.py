SECRET_KEY = 'dummy'
INSTALLED_APPS = ['memory']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = True
