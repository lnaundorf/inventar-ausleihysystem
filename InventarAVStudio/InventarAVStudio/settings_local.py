DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'database_name',                      # Or path to database file if using sqlite3.
    'USER': 'database_user',                      # Not used with sqlite3.
    'PASSWORD': 'database_password',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
  }
}

DEBUG = False

ALLOWED_HOSTS = ['*']

TEMPLATE_DEBUG = False

MEDIA_ROOT = '/path/to/media/root/'
SCHEIN_PATH = MEDIA_ROOT + 'scheine/'

STATIC_URL = 'http://static.url/static/'

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  # Uncomment the next line for simple clickjacking protection:
  # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # Uncomment the next line to enable the admin:
  'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  # 'django.contrib.admindocs',
  'Inventar',
  'Benutzer',
  'Schein',
  'Public',
  'Dashboard',
  'ClientManagement',
  'gunicorn',
)
