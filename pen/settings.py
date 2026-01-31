from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment setup
env = environ.Env(
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    CORS_ALLOWED_ORIGINS=(list, []),
)
env.read_env(str(BASE_DIR / ".env"))

SITE_ID = 1

SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key-change-in-production")
DEBUG = env("DEBUG")
SITE_URL = env("SITE_URL", default="http://localhost:8000")

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


# Database - SQLite default for Docker. Use in production
# DATABASES = {"default": env.db(default="sqlite:////app/db/db.sqlite3")}


# Database - SQLite. Use in development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data" / "db" / "db.sqlite3",
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
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
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
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# Password reset settings
PASSWORD_RESET_TIMEOUT = 86400  # 24 hours in seconds

# Add TinyMCE configuration

# ================================================================
# TINYMCE CONFIGURATION (Self-hosted, FREE plugins only)
# ==================================================================

TINYMCE_DEFAULT_CONFIG = {
    # Core settings
    "height": 650,
    "menubar": "file edit view insert format tools table help",
    "branding": False,
    "promotion": False,
    # FREE plugins only - no premium plugins = no console errors
    "plugins": [
        "advlist",  # Advanced list formatting
        "autolink",  # Auto-convert URLs to links
        "lists",  # Bullet and numbered lists
        "link",  # Insert/edit links
        "image",  # Insert/edit images
        "charmap",  # Special characters
        "preview",  # Preview content
        "anchor",  # Named anchors
        "searchreplace",  # Find and replace
        "visualblocks",  # Show block elements
        "code",  # Edit HTML source
        "fullscreen",  # Fullscreen editing
        "insertdatetime",  # Insert date/time
        "media",  # Embed videos
        "table",  # Tables
        "wordcount",  # Word count
        "help",  # Help dialog
    ],
    # Toolbar configuration
    "toolbar": (
        "undo redo | blocks | bold italic underline strikethrough | "
        "alignleft aligncenter alignright alignjustify | "
        "bullist numlist outdent indent | link image media table | "
        "code fullscreen preview | removeformat help"
    ),
    # Block formats (headings, paragraph, etc.)
    "block_formats": "Paragraph=p; Heading 2=h2; Heading 3=h3; Heading 4=h4; Blockquote=blockquote; Code=pre",
    # Image settings - allows upload and URL
    "image_advtab": True,
    "image_caption": True,
    "automatic_uploads": True,
    "file_picker_types": "image",
    "images_upload_url": "/tinymce/upload/",  # We'll create this view
    # Link settings
    "link_default_target": "_blank",
    "link_assume_external_targets": True,
    # Content styling - uses your site's CSS
    "content_css": "/static/css/tinymce-content.css",
    # Clean paste from Word
    "paste_as_text": False,
    # Security - what HTML is allowed
    "valid_elements": (
        "p,br,b,strong,i,em,u,s,strike,sub,sup,"
        "h1,h2,h3,h4,h5,h6,"
        "ul,ol,li,"
        "a[href|target|title],"
        "img[src|alt|title|width|height|class],"
        "table[border|cellspacing|cellpadding],thead,tbody,tr,th[colspan|rowspan],td[colspan|rowspan],"
        "blockquote,pre,code,"
        "div[class],span[class],"
        "hr"
    ),
    # Relative URLs (important for portability)
    "relative_urls": False,
    "remove_script_host": True,
    "document_base_url": "/",
}
