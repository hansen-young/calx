from calx.utils import import_module
from calx.scripts.runner.base import BaseRunner
from calx.utils import ValidatedFunction


class ModuleRunner(BaseRunner):
    def __init__(self, name: str, envfile: dict):
        super().__init__(name, envfile)

    def __call__(self, path: str, arguments: dict):
        klass = import_module(path)
        ValidatedFunction(klass, None).call(**arguments)()
