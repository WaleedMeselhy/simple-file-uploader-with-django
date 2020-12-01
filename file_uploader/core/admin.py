from django.contrib.admin import site

from core import models


site.register([models.File])