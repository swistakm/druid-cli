# -*- coding: utf-8 -*-
# Copyright (C) 2014 by Michał Jaworski <swistakm@gmail.com>

# This file is part of druid-cli.

# druid-cli is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# druid-cli is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with druid-cli.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import os


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), 'druid_cli', '__init__.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))

INSTALL_REQUIRES = reqs('requirements.txt')

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )
    read_md = lambda f: open(f, 'r').read()

README = os.path.join(os.path.dirname(__file__), 'README.md')
PACKAGES = find_packages('.')
PACKAGE_DIR = {'': 'src'}

setup(
    name='druid-cli',
    version=VERSION,
    author='Michał Jaworski',
    author_email='swistakm@gmail.com',
    description='Missing command line interface to druid data store.',
    long_description=read_md(README),

    packages=PACKAGES,

    url='https://github.com/swistakm/druid-cli',
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,

    license="LGPL",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
    ],

    entry_points={
        'console_scripts': [
            'druid-cli = druid_cli.cli:cli'
        ]
    }
)
