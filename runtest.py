#!/usr/bin/env python
import sys
import logging
from django.core.management import call_command

from django.conf import settings

logging.disable(logging.CRITICAL)


def configure(nose_args=None):
    if not settings.configured:
        settings.configure(
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
            TEMPLATES=[{
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            }],
            INSTALLED_APPS=[
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django_views',
                'django_views_test',
            ],
            ROOT_URLCONF='django_views_test.urls',
            NOSE_ARGS=nose_args
        )

if __name__ == '__main__':
    configure([])
    from django_nose import NoseTestSuiteRunner

    runner = NoseTestSuiteRunner()
    test_args = []

    if not test_args:
        test_args = ['django_views_test']
    num_failures = runner.run_tests(test_args)

    if num_failures:
        sys.exit(num_failures)