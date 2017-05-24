from setuptools import setup, find_packages
import os
from io import open
import versioneer


packagename = 'metasrc'
description = 'LSST project metadata synthesis and JSON-LD export library.'
author = 'Association of Universities for Research in Astronomy, Inc.'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/lsst-sqre/metasrc'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename, mode='r', encoding='utf-8').read()


long_description = read('README.rst')


setup(
    name=packagename,
    version=versioneer.get_version(),
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
        'requests>=2.13.0'
    ],
    cmdclass=versioneer.get_cmdclass()
    # package_data={},
    # entry_points={}
)
