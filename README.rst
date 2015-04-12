django-easy-app
***************

This is a django app that allows for extending the django url processing to
allow for defining url routing as part of a django Class based view.

Quickstart
==========

Here are some steps for getting things going

Set up a new django project
---------------------------
django-admin startapp *project_name*

Example:

.. code-block::
    django-admin startproject foo


Add django-easy-app to INSTALLED_APPS
-------------------------------------


Extend the project urls.py
--------------------------

Add the following two lines to the end of the project urls.py module.

.. code-block:: python
    from django_easy_app.urlmanager import app_urlpatterns
    urlpatterns += app_urlpatterns()

Create a new django-easy-app enabled project
--------------------------------------------
Use manage.py to create a new django-easy-app enabled project.

python manage.py starteasyapp *app_name*
.. code-block::
    django-admin starteasyapp fooapp

Create views
------------
In the views.py file define a variable named "easydjango" and set the value
to true.

Make sure each view that should be accessible from the web has a *route*
attribute that contains the part of the url that should be associated with the
app.  This should not include the app name.

So for example fooapp.view.ExampleView below has a route value of '' which
will cause it to be accessible at http://hostname:port/fooapp/

.. example::
    from django.http import HttpResponse
    from django.views.generic import View
    easydjango = True
    class NameView(View):
        route = ''
        def get(self, request):
            name = request.GET.get('name', 'World!')
            return HttpResponse('Hello %s' % name)
