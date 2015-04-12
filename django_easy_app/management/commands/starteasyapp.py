from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from optparse import make_option
import os


basic_urls_py = '''
from django.conf.urls import url
from django.views.generic import View
import inspect
from . import views
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


urlpatterns = []


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
    for module_name, module_class in inspect.getmembers(view_module, inspect.isclass):
        if issubclass(module_class, View):
            logger.debug('Found module: %s', module_name)
            if hasattr(module_class, 'route'):
                logger.debug('Module %s has route attribute of %r', module_class, module_class.route)
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


urlpatterns += view_urlpatterns(views)
'''

basic_views_py = '''
from django.http import HttpResponse
from django.views.generic import View

easydjango = True


class ExampleView(View):
    # This is the part of the url after the appname in the url
    route=''

    # This method returns html from a get request
    def get(self, request):
        name = request.GET.get('name', 'World!')
        return HttpResponse('Hello %s' % name)
'''

class Command(BaseCommand):
    help = 'Creates a django application that allows for creating class based '
    'views that can autoregister with urls.py'

    args = '<appname>'

    def add_arguments(self, parser):
        parser.add_argument('appname', nargs='+')

    def handle(self, *args, **options):
        if len(args):
            appname = args[0]
        else:
            appname = options['appname'][0]
        self.stdout.write('Creating easyapp named: %s', appname)
        call_command('startapp', appname)
        with open(os.path.join(appname, 'urls.py'), 'w') as fh:
            fh.write(basic_urls_py)
        with open(os.path.join(appname, "views.py"), 'w') as fh:
            fh.write(basic_views_py)
