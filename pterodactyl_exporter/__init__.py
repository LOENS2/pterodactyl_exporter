__author__ = 'LOENS2'
__license__ = 'GPL-3.0'

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("pterodactyl_exporter")
