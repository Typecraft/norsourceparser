#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'typecraft_python>=0.5.0'
]

test_requirements = [
    'typecraft_python>=0.5.0'
]

setup(
    name='norsourceparser',
    version='1.0.0-rc1',
    description="Simple conversion of Norsource-xml files into tc-xml.",
    long_description=readme + '\n\n' + history,
    author="Tormod Haugland",
    author_email='tormod.haugland@gmail.com',
    url='https://github.com/tOgg1/norsourceparser',
    packages=find_packages(),
    package_dir={'norsourceparser':
                 'norsourceparser'},
    entry_points={
        'console_scripts': [
            'norsourceparser=norsourceparser.frontend:main'
        ]
    },
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
