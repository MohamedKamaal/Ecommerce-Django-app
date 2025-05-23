
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
from decouple import config
import os 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["56.228.60.131","localhost"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'django_countries',
    'phonenumber_field',
    'cities_light',
    'users',
    'taggit',
    'cloudinary',
    'colorfield',  
    'django_extensions',
    'store',
    'cart',
    'shipping',
    'orders',
    'payments',
    'reviews',

]
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']  # English only
CITIES_LIGHT_INCLUDE_COUNTRIES = ['EG']  # Only USA and Canada
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA']  # Populated places/cities
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processsors.cart',
                'store.context_processors.categories'   
                
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),  # Fetch database name from .env file
        'USER': config('DB_USER'),  # Fetch database user from .env file
        'PASSWORD': config('DB_PASSWORD'),  # Fetch password from .env file
        'HOST': 'localhost',  # Use 'localhost' if running on the same machine, or provide the IP address of the server
        'PORT': '5432',  # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True





# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CLOUD_NAME = config("CLOUD_NAME") 
API_KEY = config("CLOUD_API_KEY")
API_SECRET = config("CLOUD_SECRET_KEY") # Click 'View API Keys' above to copy your API secret


AUTHENTICATION_BACKENDS = [
  
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
   
]


LOGIN_REDIRECT_URL = '/'  # Redirect after login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'



ACCOUNT_UNIQUE_EMAIL = True             # Enforce unique email
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # No username field

AUTH_USER_MODEL = "users.User"
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']

ACCOUNT_FORMS = {
    'login': 'users.forms.CustomLoginForm',
    'signup': 'users.forms.CustomSignupForm',
    # Add other forms as needed:
    # 'reset_password': 'accounts.forms.CustomResetPasswordForm',
    # 'change_password': 'accounts.forms.CustomChangePasswordForm',
    # 'set_password': 'accounts.forms.CustomSetPasswordForm',
    # 'reset_password_from_key': 'accounts.forms.CustomResetPasswordKeyForm',
    # 'user_token': 'accounts.forms.CustomUserTokenForm',
}

SOCIALACCOUNT_AUTO_SIGNUP = True

# Skip the signup form if possible
SOCIALACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'  # For testing, change in production

# Require email from social providers (Twitter may not provide)
SOCIALACCOUNT_EMAIL_REQUIRED = True

# stripe
STRIPE_PUBLIC_KEY=config("STRIPE_PUBLIC_KEY")
STRIPE_PRIVATE_KEY=config("STRIPE_PRIVATE_KEY")


# EMAIL 
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Use TLS for security
EMAIL_USE_SSL = False  # Do not use SSL (mutually exclusive with TLS)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


DEFAULT_FILE_STORAGE="storages.backends.s3boto3.S3Boto3Storage"
STATIC_URL = 'static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'



STATIC_ROOT = BASE_DIR / "staticfiles"
