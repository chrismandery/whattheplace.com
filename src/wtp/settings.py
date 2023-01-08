import os
import re

from settings_local import * #@UnusedWildImport

BASE_PATH = os.path.abspath(os.path.dirname(__file__) + "/../../")

# Basic Django configuration
ADMINS = ( ("Christian Mandery", "..."), )
ALLOWED_HOSTS = ("www.whattheplace.com",)
AUTH_PROFILE_MODULE = "wtp.UserProfile"
DEFAULT_FROM_EMAIL = "..."
INTERNAL_IPS = ("127.0.0.1",)
LANGUAGE_CODE = "en-us"
LOGIN_URL = "/Login/"
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(BASE_PATH, "var/media/")
MEDIA_URL = "/media/"
ROOT_URLCONF = "wtp.urls"
SECRET_KEY = "..."
SERVER_EMAIL = DEFAULT_FROM_EMAIL
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'  # necessary for OpenID authentification
STATIC_ROOT = os.path.join(BASE_PATH, "var/static/")
STATIC_URL = "/static/"
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = "Europe/Berlin"

# Authentification backends
AUTHENTICATION_BACKENDS = (
  "wtp.openid.OpenIDAuthBackend",
  "wtp.facebook.FacebookAuthBackend",
  "wtp.twitter.TwitterAuthBackend",
  "django.contrib.auth.backends.ModelBackend"
)

# Debug Toolbar panels
DEBUG_TOOLBAR_PANELS = (
  # Default panels
  "debug_toolbar.panels.versions.VersionsPanel",
  "debug_toolbar.panels.timer.TimerPanel",
  "debug_toolbar.panels.settings.SettingsPanel",
  "debug_toolbar.panels.headers.HeadersPanel",
  "debug_toolbar.panels.request.RequestPanel",
  "debug_toolbar.panels.sql.SQLPanel",
  "debug_toolbar.panels.staticfiles.StaticFilesPanel",
  "debug_toolbar.panels.templates.TemplatesPanel",
  "debug_toolbar.panels.cache.CachePanel",
  "debug_toolbar.panels.signals.SignalsPanel",
  "debug_toolbar.panels.logging.LoggingPanel",
  "debug_toolbar.panels.redirects.RedirectsPanel",
  
  # HTML Tidy/Validator Panel
  "debug_toolbar_htmltidy.panels.HTMLTidyDebugPanel",
)

# Facebook
FACEBOOK_APPID = "..."
FACEBOOK_APPSECRET = "..."

# URLs to ignore 404 errors for
IGNORABLE_404_URLS = (
  re.compile(r"^/favicon\.txt$"),
  re.compile(r"^/robots\.txt$"),
  re.compile(r"^/data/")
)

# Installed apps
INSTALLED_APPS = (
  "debug_toolbar",
  "debug_toolbar_htmltidy",
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.staticfiles",
  "south",
  "wtp"
)

# Middleware classes
MIDDLEWARE_CLASSES = (
  "debug_toolbar.middleware.DebugToolbarMiddleware",
#  "django.middleware.common.BrokenLinkEmailsMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "wtp.middleware.TrackingMiddleware"
)

# Twitter
TWITTER_CONSUMERKEY = "..."
TWITTER_CONSUMERSECRET = "..."
