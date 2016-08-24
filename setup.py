#!/usr/bin/env python

from setuptools import setup

setup_extra = {
    'cffi_modules': ["hashids_cffi/hashids_build.py:ffi"]
}

setup(
    name="hashids-cffi",
    version="0.1.0",
    description="Python wrapper for hashids.c",
    url="https://github.com/thedrow/hashids-cffi",
    author="Omer Katz",
    author_email="omer.drow@gmail.com",
    license="BSD",
    packages=["hashids_cffi"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
    **setup_extra
)
