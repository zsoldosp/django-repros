#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import changeformrepro

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = changeformrepro.__version__

if sys.argv[-1] == 'publish':
    os.system('make release')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='changeformrepro',
    version=version,
    description="""change form bug repro""",
    long_description=readme,
    author='Peter Zsoldos',
    author_email='hello@zsoldosp.eu',
    url='https://github.com/zsoldosp/changeformrepro',
    packages=[
        'changeformrepro',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='changeformrepro',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
