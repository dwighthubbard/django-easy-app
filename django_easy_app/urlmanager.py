from django.conf import settings
from django.conf.urls import include, url
from django.utils.importlib import import_module
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


def app_urlpatterns():
    """
    Iterate through the django INSTALLED_APPS and return a list of urlpatterns
    for any apps that support easydjango.
    :return:
    """
    urlpatterns = []
    for app in settings.INSTALLED_APPS:
        try:
            _view_module = import_module('%s.views' % app)
        except ImportError:
            _view_module = None

        if _view_module and hasattr(_view_module, 'easydjango'):
            if _view_module.easydjango == True:
                logger.debug('Adding urls for %s module', app)
                try:
                    _module = import_module('%s.urls' % app)
                    urlpatterns.append(url(r'^%s/' % app, include(_module)))
                except ImportError:
                    pass
    return urlpatterns
