#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

from ep import __version__


setup(
    name='ep',
    description=(
        'A tool to support an explicit contract between application '
        'and plaftorm'
    ),
    long_description=open('README.md').read(),
    version=__version__,
    author='Carles Barrobés',
    author_email='carles@barrobes.com',
    url='https://github.com/txels/ep',
    packages=['ep'],
    install_requires=['docopt', 'Fabric', 'semver'],
    entry_points=dict(
        console_scripts=[
            'ep = ep.cli:Commands.main'
        ],
    ),
    package_data={
        '': ['*.txt', '*.md'],
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
    ],
)
