#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='hitsl.utils',
    version='0.1.0',
    url='https://bitbucket.org/hitsl/hitsl.utils',
    author='hitsl',
    description='Small utilities used in HITSL',
    long_description=read('README.md'),
    include_package_data=True,
    packages=['hitsl_utils'],
    platforms='any',
    install_requires=[
        'Flask',
        'pytz',
        'Requests',
        'Blinker',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
