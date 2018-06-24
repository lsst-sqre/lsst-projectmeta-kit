import logging

from pkg_resources import get_distribution, DistributionNotFound

__all__ = ('__version__',)


try:
    __version__ = get_distribution('lsstprojectmeta').version
except DistributionNotFound:
    # Package is not installed
    __version__ = '0.0.0'

# Allow users to attach their own handlers
logging.getLogger(__name__).addHandler(logging.NullHandler())
