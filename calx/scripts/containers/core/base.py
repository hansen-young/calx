class BaseContainer:
    @property
    def pid(self) -> int:
        raise NotImplementedError()

    @property
    def exitcode(self) -> int:
        raise NotImplementedError()

    def is_running(self) -> bool:
        raise NotImplementedError()

    def is_finished(self) -> bool:
        raise NotImplementedError()

    def wait(self):
        raise NotImplementedError()

    def run(self, step_name: str, config_file: str, workdir: str, envlist: str):
        raise NotImplementedError()
