from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'padel_local',
        'USER': 'padel',
        'PASSWORD': 'padel',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = 'http://localhost:8000/media/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '501506672795-refr9doggnjb9mn61kbi6ptsbsrtqg62.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'jqoDueV57i-JvwoDFb9OEp5Q'

SOCIAL_AUTH_FACEBOOK_KEY = '1522942647965123'
SOCIAL_AUTH_FACEBOOK_SECRET = 'afff87426d95c8e7df1a70b0d877c6c1'

MANDRILL_API_KEY = 'yOqmxmaM1I9pAmevOV_Fuw'
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"