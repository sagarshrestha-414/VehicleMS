from pathlib import Path
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR=os.path.join(BASE_DIR,'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT=os.path.join(BASE_DIR,'static')





SECRET_KEY = 'ftxnh_7475z^joy_*l9t*qnqow!@)y#(541^w1=(8--=3g#4*d'


DEBUG = True


ALLOWED_HOSTS = ['localhost','127.0.0.1']



INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vehicle',
    'widget_tweaks',
    'chatbot',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'vehicleservicemanagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'vehicleservicemanagement.wsgi.application'




DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'vehicledb',

        'USER': 'postgres',

        'PASSWORD': '@9860463035',

        'HOST': 'localhost',

        'PORT': '5433',
        
 }
}
# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': 'dv7h01mj9od00',

#         'USER': 'yxonisrwlmfayu',

#         'PASSWORD': '80c59cb0a42b0187d8738108f83c6aa2d94e1aefcb30798c68bbdbd97c6e9d95',

#         'HOST': 'ec2-3-225-213-67.compute-1.amazonaws.com',

#         'PORT': '5432',
#  }
# }


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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS=[
STATIC_DIR,
 ]

LOGIN_REDIRECT_URL='/afterlogin'


EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dhojusagar619@gmail.com'
EMAIL_HOST_PASSWORD = '@Dhoju19990409'
EMAIL_RECEIVING_USER = ['saagardhoju414@gmail.com']

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'



CHATBOT_CONFIG = {
    'AI_MODEL_PATH': os.path.join(BASE_DIR, 'chatbot/ai/models'),
    'INTENTS_FILE': os.path.join(BASE_DIR, 'chatbot/ai/intents.json'),
}

