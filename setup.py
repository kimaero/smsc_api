#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='smsc_api',
    version='0.1.0',
    url='https://github.com/kimaero/smsc_api',
    author='Denis Kim',
    author_email='denis@kim.aero',
    description='Wrapper for HTTP API of smsc.ru',
    packages=find_packages(),
    install_requires=['requests >= 2.18.4'],
)
