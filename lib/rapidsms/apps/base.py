#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import sys
import os
import pkgutil

from ..utils.modules import try_import, get_class
from ..log.mixin import LoggerMixin


class AppBase(object, LoggerMixin):
    """
    """

    @classmethod
    def find(cls, app_name):
        """
        Return the RapidSMS app class from *app_name* (a standard Django
        app name), or None if it does not exist. Import errors raised
        *within* the module are allowed to propagate.
        """

        module_name = "%s.app" % app_name
        module = try_import(module_name)
        if module is None: return None
        return get_class(module, cls)


    def __init__(self, router):
        self.router = router

    def _logger_name(self): # pragma: no cover
        return "app/%s" % self.name

    @property
    def name(self):
        """
        Return the name of the module which this app was defined within.
        This can be considered a unique identifier with the project.
        """

        return self.__module__.split(".")[-2]

    @property
    def root_path(self):
        """
        Return the root path for module which this app was defined within.
        """
        return self._get_root_path()

    def _get_root_path(self):
        """Returns the path to a package or cwd if that cannot be found. This
            returns the path of a package or the folder that contains a module.
            Graciously cribbed from https://github.com/mitsuhiko/flask/blob/master/flask/helpers.py
        """
        import_name = self.__module__
        # Module already imported and has a file attribute. Use that first.
        mod = sys.modules.get(import_name)
        if mod is not None and hasattr(mod, '__file__'):
            return os.path.dirname(os.path.abspath(mod.__file__))

        # Next attempt: check the loader.
        loader = pkgutil.get_loader(import_name)

        # Loader does not exist or we're referring to an unloaded main module
        # or a main module without path (interactive sessions), go with the
        # current working directory.
        if loader is None or import_name == '__main__':
            return os.getcwd()

        # For .egg, zipimporter does not have get_filename until Python 2.7.
        # Some other loaders might exhibit the same behavior.
        if hasattr(loader, 'get_filename'):
            filepath = loader.get_filename(import_name)
        else:
            # Fall back to imports.
            __import__(import_name)
            filepath = sys.modules[import_name].__file__

        # filepath is import_name.py for a module, or __init__.py for a package.
        return os.path.dirname(os.path.abspath(filepath))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<app: %s>" %\
            self.name

    # router events
    def start (self): pass
    def stop  (self): pass

    # incoming phases
    def filter   (self, msg): pass
    def parse    (self, msg): pass
    def handle   (self, msg): pass
    def default  (self, msg): pass
    def catch    (self, msg): pass
    def cleanup  (self, msg): pass

    # outgoing phases:
    def outgoing (self, msg): pass
