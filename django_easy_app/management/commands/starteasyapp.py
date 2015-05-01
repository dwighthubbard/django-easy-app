from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from optparse import make_option
import os


class DJangoEasyAppError(Exception):
    pass


urls_addition = """
# Added by django_easy_app
from . import views
from django_easy_app.urlmanager import view_urlpatterns
urlpatterns += view_urlpatterns(views)
"""
views_addition = """
# Added by django_easy_app
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
"""

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
        self.stdout.write('Creating easyapp named: %s' % appname)
        call_command('startapp', appname)
        urls_filename = os.path.join(appname, 'urls.py')
        views_filename = os.path.join(appname, 'views.py')
        urls_data = """from django.conf.urls import url

urlpatterns = []
        """
        views_data = ''

        # Read in the source files

        if os.path.exists(urls_filename):
            with open(urls_filename) as urls_file:
                urls_data = urls_file.read()
        if os.path.exists(views_filename):
            with open(views_filename) as views_file:
                views_data = views_file.read()

        # Add our integration
        urls_data += urls_addition

        views_data += views_addition

        # Write out the updated files
        if urls_data:
            with open(urls_filename, 'w') as urls_file:
                urls_file.write(urls_data)

        if os.path.exists(views_filename):
            with open(views_filename, 'w') as views_file:
                views_file.write(views_data)