# -*- coding: utf-8 -*-
import os
# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from setuptools import setup, find_packages

README = '''
This is a Python binding for groupcache.

Groupcache is a distributed caching and cache-filling library, intended as a replacement for a pool of memcached nodes in many cases.

For more information, please visit the [GitHub repository](https://github.com/amazingchow/groupcache-py).
'''

setup(
    name='pygroupcache',
    version='1.0.0',
    description='A Python binding for groupcache',
    long_description=README,
    author='Adam Zhou',
    author_email='adamzhouisnothing@gmail.com',
    url='https://github.com/amazingchow/groupcache-py',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add any dependencies here
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': []
    }
)
