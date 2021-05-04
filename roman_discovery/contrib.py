"""
Helper functions copied as-is from Werkzeug utils.

Ref: https://github.com/pallets/werkzeug/blob/master/src/werkzeug/utils.py

:copyright: 2007 Pallets
:license: BSD-3-Clause
"""

import pkgutil
from importlib import import_module


def find_modules(import_path, include_packages=False, recursive=False):
    """
    Finds all the modules below a package.

    This can be useful to
    automatically import all views / controllers so that their metaclasses /
    function decorators have a chance to register themselves on the
    application.

    Packages are not returned unless `include_packages` is `True`.  This can
    also recursively list modules but in that case it will import all the
    packages to get the correct load path of that module.

    :param import_path: the dotted name for the package to find child modules.
    :param include_packages: set to `True` if packages should be returned, too.
    :param recursive: set to `True` if recursion should happen.
    :return: generator
    """
    module = import_module(import_path)
    path = getattr(module, "__path__", None)
    if path is None:
        raise ValueError("%r is not a package" % import_path)
    basename = module.__name__ + "."
    for _importer, modname, ispkg in pkgutil.iter_modules(path):
        modname = basename + modname
        if ispkg:
            if include_packages:
                yield modname
            if recursive:
                for item in find_modules(modname, include_packages, True):
                    yield item
        else:
            yield modname
