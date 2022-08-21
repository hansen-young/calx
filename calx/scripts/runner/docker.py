from calx.scripts.runner.base import BaseRunner
from calx.scripts.containers import DockerContainer


class DockerRunner(BaseRunner):
    def __init__(self, name: str, envfile: str):
        super().__init__(name, envfile)
        self.cnt = DockerContainer()

    def __call__(self, **options):
        self.cnt._process = self.cnt._client.containers.run(
            **options,
            auto_remove=False,
            detach=True,
            environment=self.envlist,
        )
        self.cnt._container_id = self.cnt._process.short_id
        self.cnt._spawn_logging_thread()
        self.cnt.wait()
