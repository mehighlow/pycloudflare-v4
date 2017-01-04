#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='pycloudflare-v4',
    version='0.8.1',
    description='Python wrapper for CloudFlare API v4',
    url='https://github.com/zmgit/pycloudflare-v4',
    author='Michael Zaglada',
    author_email='zmpbox@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: DevOps, Sysadmins, Developers',
        'Topic :: Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='CludFlare API v4 wrapper',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'build', 'dist'])
)
