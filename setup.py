#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'typecraft-python'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='norsourceparser',
    version='0.1.0',
    description="Simple conversion of Norsource-xml files into tc-xml.",
    long_description=readme + '\n\n' + history,
    author="Tormod Haugland",
    author_email='tormod.haugland@gmail.com',
    url='https://github.com/tOgg1/norsourceparser',
    packages=[
        'norsourceparser',
    ],
    package_dir={'norsourceparser':
                 'norsourceparser'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='norsourceparser',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
