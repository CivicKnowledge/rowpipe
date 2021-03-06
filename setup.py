#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages, setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development :: Debuggers',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='rowpipe',
    version='0.2.0',
    description='Generate row data from a variety of file formats',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        'tabulate',
        'decorator',
        'codegen',
        'geoid',
        'meta',
        'python-dateutil',
        'rowgenerators'],
    author="Eric Busboom",
    author_email='eric@civicknowledge.com',
    url='https://github.com/Metatab/rowgenerator.git',
    license='MIT',
    classifiers=classifiers
)
