from logging import log
import os
from whitenoise import WhiteNoise
import logging
import logging.config
from django.core.wsgi import get_wsgi_application


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": ("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "": {
            "level": "ERROR",
            "handlers": ["console"],
        },
        "custom": {
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.access": {
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
            "handlers": ["console"],
            "propagate": False,
        },
        "gunicorn.error": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

logging.config.dictConfig(logging_config)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

application = get_wsgi_application()


application = WhiteNoise(application, root=os.path.join(PROJ_DIR, "static"))
