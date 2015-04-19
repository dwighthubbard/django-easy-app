from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from optparse import make_option
import os


class DJangoEasyAppError(Exception):
    pass


urls_addition = """
# Added by django_easy_app
from django_easy_app.urlmanager import app_urlpatterns
urlpatterns += app_urlpatterns()
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
        urls_data = None
        views_data = None

        # Read in the source files
        with open(urls_filename) as urls_file:
            urls_data = urls_file.read()
        with open(views_filename) as views_file:
            views_data = views_file.read()

        if not urls_data or not views_data:
            raise DJangoEasyAppError(
                'Unable to find the application source file'
            )

        # Add our integration
        urls_data += urls_addition

        # Write out the updated files
        if urls_data:
            with open(urls_filename, 'w') as urls_file:
                urls_file.write(urls_data)
