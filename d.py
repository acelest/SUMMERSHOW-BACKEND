
# from pathlib import Path
# import os
# from dotenv import load_dotenv

# # Charger les variables d'environnement à partir du fichier .env
# load_dotenv()

# # Configuration de la clé API
# API_PAYMENT_KEY = os.getenv("API_PAYMENT_KEY")

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-i8_h#fo^&!dbad&h89_*k%i*5pk06-62b(7^xncvk2z_o@l52_'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False

# ALLOWED_HOSTS = ["*"]

# JAZZMIN_SETTINGS = {
#     "site_title": "TheSummer Show",
#     "site_header": "TheSummer Show",
#     "site_brand": "TheSummer Show",
# }

# # Application definition


# #aws configurations


# AWS_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('R2_STORAGE_BUCKET_NAME')
# AWS_S3_ENDPOINT_URL = 'https://a47b4fa647b5c8c98f04f720c123e23d.r2.cloudflarestorage.com'
# AWS_S3_SIGNATURE_VERSION = 's3v4'



# # Set S3 configurations for django-storages
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_LOCATION = 'media'

# # Storage settings
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# INSTALLED_APPS = [
#     'corsheaders',
#     'jazzmin',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'drf_yasg',
#     'django.contrib.staticfiles',
#     'listings',
#     # 'paiements'
#     "rest_framework",
#     "gunicorn",
#     "whitenoise"
# ]

# ADMIN_SITE_HEADER = "TheSummerShow"

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     "whitenoise.middleware.WhiteNoiseMiddleware",
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'voteapp.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'voteapp.wsgi.application'

# # Database
# # https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# # Password validation
# # https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

# # Internationalization
# # https://docs.djangoproject.com/en/5.0/topics/i18n/

# # LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'fr-fr'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True

# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'static/'

# # Default primary key field type
# # https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # CORS settings
# CORS_ALLOW_ALL_ORIGINS = True

# # For a more restrictive setting, use:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]


# # source venv/bin/activate python3 -m venv venv


# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# STATIC_ROOT = BASE_DIR / "staticfiles"