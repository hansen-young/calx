import os
import sys
import time
import subprocess

from calx.scripts.containers.core.base import BaseContainer


class LocalContainer(BaseContainer):
    def __init__(self):
        self._process = None
        self._output = None
        self.__started = False

    def __del__(self):
        if self._output and os.path.isfile(self._output):
            os.remove(self._output)

    @property
    def pid(self) -> int:
        if not self._process:
            return None
        return self._process.pid

    @property
    def exitcode(self) -> int:
        if not self._process:
            return None
        return self._process.returncode

    def is_running(self) -> bool:
        if not self._process:
            return False
        return self._process.poll() == None

    def is_finished(self) -> bool:
        return self.__started and not self.is_running()

    def output(self) -> str:
        if not self._output or not self.is_finished():
            return ""

        with open(self._output, "r") as fp:
            return fp.read()

    def wait(self, timeout: int = None):
        self._process.wait(timeout=timeout)

    def run(
        self,
        step_name: str,
        config_file: str,
        workdir: str,
        envlist: str,
        output: str = None,
    ):
        if self.__started:
            raise Exception("container has been used")

        if output:
            self._output = os.path.join(workdir, output)

        self.__started = True
        self._process = subprocess.Popen(
            [
                "python",
                "-m",
                "calx.scripts.runner.main",
                "-f",
                os.path.abspath(config_file),
                "-s",
                step_name,
            ],
            env={**os.environ, **envlist},
            cwd=workdir,
        )
