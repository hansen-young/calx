import os


class BaseRunner:
    def __init__(self, name: str, envlist: dict, workdir: str):
        if not envlist:
            envlist = {}

        if not workdir:
            workdir = "."

        self.name = name
        self.envlist = envlist
        self.workdir = os.path.abspath(workdir)
        self.__started = False

    @property
    def pid(self) -> int:
        raise NotImplementedError()

    @property
    def status_code(self) -> int:
        raise NotImplementedError()

    def is_running(self) -> bool:
        raise NotImplementedError()

    def is_finished(self) -> bool:
        raise NotImplementedError()

    # def set_environment(self, envlist: dict):
    #     raise NotImplementedError()

    # def set_working_dir(self, workdir: str):
    #     raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()
