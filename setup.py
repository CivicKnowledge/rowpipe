#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import find_packages
import uuid
import imp

from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

# Avoiding import so we don't execute __init__.py, which has imports
# that aren't installed until after installation.
ambry_meta = imp.load_source('_meta', 'rowpipe/_meta.py')

packages = find_packages()


install_requires = parse_requirements('requirements.txt', session=uuid.uuid1())

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
    version=ambry_meta.__version__,
    description='Generate row data from a variety of file formats',
    long_description=readme,
    packages=packages,
    install_requires = [
        'pyfs',
        'tabulate',
        'decorator',
        'codegen',
        'geoid',
        'meta',
        'six',
        'python-dateutil',
        'tableintuit',
        'rowgenerators'],
    author=ambry_meta.__author__,
    author_email='eric@civicknowledge.com',
    url='https://github.com/CivicKnowledge/rowgenerator.git',
    license='MIT',
    classifiers=classifiers
)
