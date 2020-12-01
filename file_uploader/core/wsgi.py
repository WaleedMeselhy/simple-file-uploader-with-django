import os
from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

application = get_wsgi_application()


application = WhiteNoise(application, root=os.path.join(PROJ_DIR, "static"))
