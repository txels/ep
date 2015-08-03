#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import os

from ep import __version__
from ep.python import Python


DIR = os.path.dirname(__file__)

runtime_dependencies = Python.read_requirements(
    os.path.join(DIR, 'requirements', 'runtime.txt')
)


if __name__ == '__main__':
    setup(
        name='ep',
        description=(
            'A tool to support an explicit contract between application '
            'and plaftorm'
        ),
        long_description=open(os.path.join(DIR, 'README.md')).read(),
        version=__version__,
        author='Carles Barrobés',
        author_email='carles@barrobes.com',
        url='https://github.com/txels/ep',
        packages=['ep'],
        install_requires=runtime_dependencies,
        entry_points=dict(
            console_scripts=[
                'ep = ep.cli:Commands.main',
            ],
        ),
        package_data={
            '': ['*.txt', '*.md'],
        },
        classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Libraries',
        ],
    )
