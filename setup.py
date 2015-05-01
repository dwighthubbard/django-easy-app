#!/usr/bin/env python

from __future__ import print_function
import os
import json
import logging
from setuptools import setup


logger = logging.getLogger(__name__)
METADATA_FILENAME = 'django_easy_app/package_metadata.json'
BASEPATH = os.path.dirname(os.path.abspath(__file__))


def readme():
    """
    Return the data from the README file in the current directory
    :return:
    """
    with open('README.rst') as f:
        return f.read()


def scripts():
    """
    Return a list of script files in the scripts directory
    :return:
    """
    script_list = []
    if os.path.isdir('scripts'):
        script_list = [
            os.path.join('scripts', f) for f in os.listdir('scripts')
        ]
    return script_list


# Create a dictionary of our arguments, this way this script can be imported
#  without running setup() to allow external scripts to see the setup settings.
setup_arguments = {
    'name': 'django-easy-app',
    'version': '0.0.1',
    'author': 'Dwight Hubbard',
    'author_email': 'd@d-h.us',
    'url': 'https://github.com/dwighthubbard/django-easy-app',
    'license': 'BSD',
    'packages': [
        'django_easy_app', 
        'django_easy_app.management',
        'django_easy_app.management.commands'
    ],
    'description': 'Extend django-admin to create apps that are easier to set',
    'install_requires': ['django'],
    'requires': ['django'],
    'long_description': readme(),
    'classifiers': [
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            'Operating System :: POSIX',
            'Programming Language :: C',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Software Development :: Libraries',
            'Topic :: System :: Systems Administration',
            'Topic :: Utilities',
    ],
    'package_data': {
        'django_easy_app': ['package_metadata.json'],
    },
    'include_package_data': True,
}


class Git(object):
    version_list = ['0', '7', '0']

    def __init__(self, version=None):
        if version:
            self.version_list = version.split('.')

    @property
    def version(self):
        """
        Generate a Unique version value from the git information
        :return:
        """
        git_rev = len(os.popen('git rev-list HEAD').readlines())
        if git_rev != 0:
            self.version_list[-1] = '%d' % git_rev
        version = '.'.join(self.version_list)
        return version

    @property
    def branch(self):
        """
        Get the current git branch
        :return:
        """
        return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    @property
    def hash(self):
        """
        Return the git hash for the current build
        :return:
        """
        return os.popen('git rev-parse HEAD').read().strip()

    @property
    def origin(self):
        """
        Return the fetch url for the git origin
        :return:
        """
        for item in os.popen('git remote -v'):
            split_item = item.strip().split()
            if split_item[0] == 'origin' and split_item[-1] == '(push)':
                return split_item[1]


def get_and_update_metadata():
    """
    Get the package metadata or generate it if missing
    :return:
    """
    global METADATA_FILENAME
    global REDIS_SERVER_METADATA

    if not os.path.exists('.git') and os.path.exists(METADATA_FILENAME):
        with open(METADATA_FILENAME) as fh:
            metadata = json.load(fh)
    else:
        git = Git(version=setup_arguments['version'])
        metadata = {
            'git_version': git.version,
            'git_origin': git.origin,
            'git_branch': git.branch,
            'git_hash': git.hash,
            'version': git.version,
        }
        with open(METADATA_FILENAME, 'w') as fh:
            json.dump(metadata, fh, indent=4)
    return metadata


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Update the setup arguments with our version number
    metadata = get_and_update_metadata()
    setup_arguments['version'] = metadata['version']

    # Add any scripts that should be part of the package
    if scripts():
        setup_arguments['scripts'] = scripts()

    setup(**setup_arguments)
