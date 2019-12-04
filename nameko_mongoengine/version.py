"""
Version for nameko_mongoengine package
"""

__version__ = '0.1.1'  # pragma: no cover


def version_info():  # pragma: no cover
    """
    Get version of nameko_mongoengine package as tuple
    """
    return tuple(map(int, __version__.split('.')))  # pragma: no cover
