import os
import sys
from multiprocessing import Process

from .base import BaseRunner
from calx.scripts.utils import _import_module


class ModuleRunner(BaseRunner):
    def __init__(
        self,
        path: str,
        arguments: dict,
        name: str = None,
        envlist: dict = {},
        workdir: str = None,
    ):
        super().__init__(name, envlist, workdir)
        self._path = path
        self._args = arguments
        self._process = None

    @property
    def pid(self) -> int:
        if not self._process:
            return None
        return self._process.pid

    @property
    def status_code(self) -> int:
        if not self._process:
            return None
        return self._process.exitcode

    def is_running(self) -> bool:
        if not self._process:
            return False
        return self._process.is_alive()

    def is_finished(self) -> bool:
        return self.__started and not self.is_running()

    def _set_environment(self):
        for k, v in self.envlist.items():
            os.environ[k] = v

    def _set_workdir(self):
        if self.workdir:
            sys.path.append(self.workdir)

    def _main(self):
        self._set_workdir()
        self._set_environment()

        klass = _import_module(self._path)
        klass(**self._args)()

    def __call__(self, *args, **kwargs):
        self._process = Process(target=self._main)
        self._process.start()
        self.__started = True
