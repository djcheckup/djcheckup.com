from .settings import *  # noqa

# Use an in-memory database for testing
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
