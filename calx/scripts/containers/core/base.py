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

    def output(self) -> str:
        raise NotImplementedError()

    def wait(self, timeout: int = None):
        raise NotImplementedError()

    def run(
        self,
        step_name: str,
        config_file: str,
        workdir: str,
        envlist: str,
        output: str = None,
    ):
        raise NotImplementedError()
