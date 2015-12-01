# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='wagtail-streamfieldtools',
    packages=find_packages(),
    version='0.1',
    author=u'Jonathan Ellenberger',
    author_email='jonathan_ellenberger@wgbh.org',
    url='http://github.com/WGBH/wagtail-streamfieldtools/',
    license='MIT License, see LICENSE',
    description="A suite of tools that extends Wagtail's already-awesome "
                "StreamField to make it even more flexible/versatile/useful!",
    long_description=open('README.rst').read(),
    zip_safe=False,
    install_requires=['wagtail>=1.2'],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 3 - Alpha'
    ]
)
