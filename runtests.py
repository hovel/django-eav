#!/usr/bin/env python
import sys
from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        SITE_ID = 1,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.auth',
            'eav',
            'eav.tests',
            ],
        ROOT_URLCONF='',
        DEBUG=False,
        USE_TZ=True,
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests(*test_args):
    if not test_args:
        test_args = ['eav']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = DjangoTestSuiteRunner(verbosity=2).run_tests(test_args, interactive='--no-input' not in sys.argv)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
