# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name='django-url-wrapper',
    version='0.0.1',
    description='Urlwrapper wraps urls in a text string with <a> html tags and shorten the representations',
    long_description=open('README.md').read(),
    author='CeShine Lee',
    author_email='ceshine@ceshine.net',
    url='https://github.com/ceshine/django-url-wrapper',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
