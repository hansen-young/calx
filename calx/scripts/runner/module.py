from calx.utils import import_module


class ModuleRunner:
    def __init__(self, path: str, arguments: dict):
        self._path = path
        self._args = arguments

    def __call__(self):
        klass = import_module(self._path)
        klass(**self._args)()
