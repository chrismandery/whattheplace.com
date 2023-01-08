# Miscellaneous parameters
DEBUG = True
BASE_URL = "http://localhost:8000"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
DATABASES = {
    "default": {
	"ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/home/chris/wtp/sqlite.db"
    }
}
