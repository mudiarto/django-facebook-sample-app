# Django settings for django_facebook_sample_app project.
import os
#import sys
from path import path


DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = path(__file__).abspath().dirname()

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

# ADMIN_MEDIA_PREFIX = '' # SEE DEFINITION IN STATICFILES SETTINGS

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i=6&ymfrh1ib38^9exo=4qcs&$pj$wav10@^5*nj@sf0-6otov'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # facebook middleware
    'runwithfriends.facebook.FacebookMiddleware',
)


ROOT_URLCONF = 'django_facebook_sample_app.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'staticfiles.context_processors.static_url', # django-staticfiles requirement
  'runwithfriends.context_processors.facebook', # helper for facebook
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # staticfiles - remove it in 1.3
    'staticfiles',

    # third party
    'social_auth', # added social-auth backend

    # our app
    'runwithfriends', 
)

############################################################
# social-auth settings
# according to instruction in :https://github.com/omab/django-social-auth
############################################################

# added social_auth backend to AUTHENTICATION_BACKEND
AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    #'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# The application will try to import custom backends from the sources defined in:
#  This way it's easier to add new providers, check the already defined ones in social_auth.backends for examples.
# Take into account that backends must be defined in AUTHENTICATION_BACKENDS or Django won't pick them when trying to authenticate the user.
SOCIAL_AUTH_IMPORT_BACKENDS = (
    'myproy.social_auth_extra_services',
)

# Setup login URLs:
LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL    = '/login-error/'

# In case of authentication error, the message can be stored in session if the following setting is defined:
SOCIAL_AUTH_ERROR_KEY = 'social_errors'

# Not mandatory, but recommended:
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'

# Configure authentication and association complete URL names to avoid possible clashes:
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'associate_complete'

############################################################
# end social-auth settings
############################################################


############################################################
# staticfiles settings
############################################################
SERVE_MEDIA = DEBUG  # only serve media when debug is on
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static/")
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "media/"),
)
############################################################
# end staticfiles settings
############################################################

############################################################
# import local settings. 
# You need to copy local_settings.py.template to 
# local_settings.py, and fill the information there
############################################################
try:
    from local_settings import *
except:
    pass
