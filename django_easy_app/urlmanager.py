from django.conf import settings
from django.conf.urls import patterns, include, url
from django.utils.importlib import import_module
from django.views.generic import View

import inspect
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


def app_urlpatterns():
    """
    Iterate through the django INSTALLED_APPS and return a list of urlpatterns
    for any apps that support django-easy-app.
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


def view_urlpatterns(view_module, base_url_path=None):
    """
    Iterates a view module for class based views that have a "route" attribute
    and use it to create a url patter.
    :param view_module:
    :param base_url_path:
    :return: list urlpatterns
    """
    view_name = '.'.join(view_module.__name__.split('.')[:-1])
    view_patterns = []
    for module_name, module_class in inspect.getmembers(
            view_module, inspect.isclass
    ):
        if issubclass(module_class, View):
            logger.debug('Found module: %s', module_name)
            if hasattr(module_class, 'route'):
                logger.debug(
                    'Module %s has route attribute of %r',
                    module_class, module_class.route
                )
                regex = '^{0}$'.format(module_class.route)
                arguments = inspect.getargspec(module_class.get).args
                arguments.remove('self')
                arguments.remove('request')
                if arguments:
                    pass
                else:
                    view_patterns.append(
                        url(
                            regex,
                            module_class.as_view(),
                            name=module_name
                        )
                    )
    return view_patterns
