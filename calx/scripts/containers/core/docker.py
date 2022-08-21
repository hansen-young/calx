import os
import docker
from threading import Thread
from calx.logger import create_logger
from calx.logger import default_logger as log
from calx.scripts.containers.core.base import BaseContainer


class DockerContainer(BaseContainer):
    def __init__(self):
        self._client = docker.from_env()
        self._process = None
        self._container_id = None
        self.__started = False

        self._logger = create_logger("calx-docker")
        self._logging_thread = None

    def __del__(self):
        if self._process == None:
            return

        if self.is_running():
            self._process.stop()

        self._process.remove()

    def _stats(self) -> dict:
        # Note: docker sdk does not update the container attributes returned by
        # container.run, we need to manually get the container.
        return self._client.containers.get(self._container_id).attrs

    def _read_log(self):
        for line in self._process.logs(stream=True, follow=True):
            self._logger.info(line)

    def _spawn_logging_thread(self):
        self._logging_thread = Thread(target=self._read_log)
        self._logging_thread.start()

    @property
    def pid(self) -> int:
        if not self._process:
            return None
        return self._stats()["State"]["Pid"]

    @property
    def exitcode(self) -> int:
        if not self._process:
            return None
        return self._stats()["State"]["ExitCode"]

    def is_running(self) -> bool:
        if not self._process:
            return False
        return self._stats()["State"]["Running"]

    def is_finished(self) -> bool:
        return self.__started and not self.is_running()

    def wait(self, timeout: int = None):
        if isinstance(timeout, int) and timeout > 0:
            self._process.wait(timeout=timeout)
        else:
            self._process.wait(condition="not-running")

    def run(self, step_name: str, envlist: dict, **kwargs):
        if self.__started:
            raise Exception("container has been used")

        self._logger.name = "calx-docker-" + step_name.replace("_", "-")

        # Note: this is the path specified in calx.scripts.containers.builders.DockerBuilder
        config_file = "/tmp/calx-run/pipeline.yaml"
        workdir = "/usr/src/app"

        # Note: auto_remove set to False, so that _stats method still can get the
        # container info even after the container exited.
        log.info(f"creating docker container for step `{step_name}`")
        self.__started = True
        self._process = self._client.containers.run(
            image=os.environ["CALX_DOCKER_IMAGE_TAG"],
            command=[
                "python",
                "-u",  # unbuffered, to stream docker logs
                "-m",
                "calx.scripts.runner.main",
                "-f",
                config_file,
                "-s",
                step_name,
            ],
            environment=envlist,
            working_dir=workdir,
            detach=True,
            auto_remove=False,
        )
        self._container_id = self._process.short_id
        self._spawn_logging_thread()
        log.info(f"successfully created container for step `{step_name}`")
