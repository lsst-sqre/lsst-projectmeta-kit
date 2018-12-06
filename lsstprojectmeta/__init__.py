import logging

from pkg_resources import get_distribution, DistributionNotFound

__all__ = ('__version__',)


try:
    __version__ = get_distribution('lsst-projectmeta-kit').version
except DistributionNotFound:
    # Package is not installed
    __version__ = 'unknown'

# Allow users to attach their own handlers
logging.getLogger(__name__).addHandler(logging.NullHandler())
