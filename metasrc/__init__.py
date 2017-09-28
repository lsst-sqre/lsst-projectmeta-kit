import logging

# Version string provided by versioneer
# https://github.com/warner/python-versioneer
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# Allow users to attach their own handlers
logging.getLogger(__name__).addHandler(logging.NullHandler())
