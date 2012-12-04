#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="watchlion",
      version="0.1",
      description="Filesystem events monitoring",
      long_description=open('README.rst').read(),
      author="ENDOH takanao",
      license="MIT",
      url="http://github.com/MiCHiLU/watchlion",
      keywords=' '.join([
        'python',
        'filesystem',
        'monitoring',
        'monitor',
        'FSEvents',
        ]
      ),
      classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
        ],
      py_modules=['watchlion'],
      install_requires=['PyYAML', 'MacFSEvents'],
      entry_points={
        'console_scripts': [
          'watchlion = watchlion:main',
          ]
      },
      zip_safe=False,
)
