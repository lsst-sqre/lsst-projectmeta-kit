from setuptools import setup, find_packages
import os
from io import open


packagename = 'lsst-projectmeta-kit'
description = ("Python toolkit for extracting and transforming metadata "
               "about LSST's code and documentation projects, and loading "
               "it into the LSST projectmeta database.")
author = 'Association of Universities for Research in Astronomy, Inc.'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/lsst-projectmeta-kit'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename, mode='r', encoding='utf-8').read()


long_description = read('README.rst')


setup(
    name=packagename,
    use_scm_version=True,
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
    install_requires=[
        'pyjwt>=1.4.2',
        'requests>=2.13.0',
        'pypandoc>=1.4',
        'panflute==1.10.6',
        'aiohttp>=2.2.5',
        'pybtex>=0.21',
        'GitPython>=2.1.7',
        'pytz',
        'motor>=1.2.0, <1.3.0'
    ],
    extras_require={
        'dev': [
            # Development/testing dependencies
            'pytest==3.2.5',
            'pytest-cov==2.5.0',
            'pytest-flake8==0.9.1',
        ]},
    setup_requires=[
        'setuptools-scm==1.15.6',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            ('lsstprojectmeta-deparagraph '
             '= lsstprojectmeta.pandoc.filters.deparagraph:main'),
            ('lsstprojectmeta-ingest-docs '
             '= lsstprojectmeta.cli.ingestdocs:main')
        ]
    }
)
