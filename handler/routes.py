# -*-coding:utf-8 -*-


from tornado.web import url
from pkgutil import iter_modules
from importlib import import_module


class Route:

    _routes = []

    def __init__(self, uri, name=None):
        self.uri = uri
        self.name = name

    def __call__(self, _handler):
        name = self.name and self.name or _handler.__name__
        self._routes.append(url(self.uri, _handler, name=name))
        return _handler

    @classmethod
    def get_route(cls):
        return cls._routes


def get_routes():
    return __name__.rsplit('.', 1)[0]


def walk_modules(path=None):
    if not path:
        path = get_routes()

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


walk_modules()