from pathlib import Path
import environ
import os


# Initialize environment variables
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Load the .env file
ENV_FILE = ".env"
environ.Env.read_env(os.path.join(BASE_DIR, ENV_FILE))

SITE_ID = 1

SITE_URL = "www.penandipublishing.com"

SECRET_KEY = env("SECRET_KEY", default="your-secret-key-here")

ALLOWED_HOSTS = [
    "65.108.89.200",
    "www.penandipublishing.com",
    "localhost",
    "127.0.0.1",
    "penandipublishing.com",
    "penandipublishing.co.uk",
    "www.penandipublishing.co.uk",
]

CSRF_TRUSTED_ORIGINS = [
    "https://65.108.89.200",
    "https://www.penandipublishing.com",
    "https://penandipublishing.com",
    "https://penandipublishing.co.uk",
    "https://www.penandipublishing.co.uk",
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/profile/"
LOGOUT_REDIRECT_URL = "/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST", default="localhost"),
        "PORT": env("DATABASE_PORT", default="5432"),
    }
}


# Application definition

INSTALLED_APPS = [
    "adminita",
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sitemaps",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "widget_tweaks",
    "tinymce",
    "prompt",
    "accounts",
    "blog",
    "core",
    "redirects",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "redirects.middleware.RedirectMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "pen.wp_redirects.WordPressRedirectMiddleware",
]

ROOT_URLCONF = "pen.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "js_asset.context_processors.importmap",
            ],
        },
    },
]

WSGI_APPLICATION = "pen.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# WhiteNoise configuration
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# WhiteNoise configuration (if you're using WhiteNoise)
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

# Media settings
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# Authentication backends to include email login
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "accounts.authentication.EmailAuthBackend",
]


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "localhost"  # Using local mail server
EMAIL_PORT = 25  # Standard SMTP port
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
CONTACT_EMAIL = env("CONTACT_EMAIL")

# Security settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# For development only
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Password reset settings
PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds

# Add TinyMCE configuration
TINYMCE_DEFAULT_CONFIG = {
    "height": 660,
    "width": "auto",
    "forced_root_block": "p",
    "remove_trailing_brs": False,
    "end_container_on_empty_block": True,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "block_formats": "Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Preformatted=pre",
    "selector": "textarea",
    "theme": "silver",
    "plugins": """
        save link image media preview codesample
        table code lists fullscreen insertdatetime nonbreaking
        directionality searchreplace wordcount visualblocks
        visualchars autolink charmap
        anchor pagebreak
        """,
    "toolbar1": """
        formatselect | fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
        """,
    "toolbar2": """
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor | code |
        """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
}

from logging_config import LOGGING  # noqa: F401, E402
