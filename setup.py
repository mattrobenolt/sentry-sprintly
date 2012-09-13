#!/usr/bin/env python
"""
sentry-sprintly
==============

An extension for Sentry which integrates with Sprint.ly.

:copyright: (c) 2012 by Matt Robenolt, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-sprintly',
    version='0.1.4',
    author='Matt Robenolt',
    author_email='matt@ydekproductons.com',
    url='http://github.com/mattrobenolt/sentry-sprintly',
    description='A Sentry extension which integrates with Sprint.ly',
    long_description=__doc__,
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sprintly = sentry_sprintly',
        ],
        'sentry.plugins': [
            'sprintly = sentry_sprintly.plugin:SprintlyPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
