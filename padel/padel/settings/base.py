from unipath import Path
BASE_DIR = Path(__file__).ancestor(3)

SECRET_KEY = '5w^vmihsy-%v-w)4!@zk@@euy0-kl7n3wkbgg4ypmt2s6^dw)z'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []

DJANGO_APPS = (
		'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	)

LOCAL_APPS = (
		'apps.users',
        'apps.torneos',
	)

THIRD_PARTY_APPS = (
        'djrill',
		'social.apps.django_app.default',
	)


INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'padel.urls'

WSGI_APPLICATION = 'padel.wsgi.application'

LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = BASE_DIR.child('media')

SOCIAL_AUTH_USER_MODEL = 'users.User'
AUTH_USER_MODEL = 'users.User'

########## PYTHON SOCIAL AUTH #############
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'apps.users.backends.EmailOrUsernameModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    # 'apps.users.pipelines.get_user_avatar',
    'apps.users.pipelines.create_player',
    'apps.users.pipelines.user_details',
)

from django.core.urlresolvers import reverse_lazy
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = reverse_lazy('welcome')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']