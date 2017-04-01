from setuptools import setup, find_packages
import os
from io import open


packagename = 'dochub-adapter'
description = 'LSST DocHub metadata gathering and JSON-LD export library.'
author = 'LSST SQuaRE'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/dochub-adapter'
version = '0.0.1'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename, mode='r', encoding='utf-8').read()


long_description = read('README.rst')


setup(
    name=packagename,
    version=version,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='lsst',
    packages=find_packages(exclude=['docs', 'tests*', 'data']),
    install_requires=[],
    # package_data={},
    # entry_points={}
)
