import os
from background_task import background
from elasticsearch import Elasticsearch
from core.models import File
import textract

import logging
import logging.config

es = Elasticsearch([os.environ["ELASTICSEARCH_HOST"]])


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
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger("custom")
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@background(schedule=1)
def parse_pdf(file_id):

    file_saved = File.objects.get(id=file_id)
    text = textract.process(PROJ_DIR + file_saved.file_path).decode()
    e1 = {"content": text, "file_id": file_id}

    res = es.index(index="files", doc_type="content", body=e1)
