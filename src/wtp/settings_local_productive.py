# Miscellaneous parameters
DEBUG = False
BASE_URL = "http://www.whattheplace.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Database
DATABASES = {
    "default": {
	"ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "whattheplace",
        "PASSWORD": "",
        "USER": "whattheplace"
    }
}
