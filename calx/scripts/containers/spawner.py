from calx.dtypes import *
from calx.scripts.containers.core import BaseContainer, LocalContainer, DockerContainer


__containers = {
    "local": LocalContainer,
    "docker": DockerContainer,
}


def spawn_container(
    container_type: str, step_name: str, config_file: str, workdir: str, envlist: dict
) -> BaseContainer:
    container = __containers[container_type]()
    container.run(step_name, config_file, workdir, envlist)

    return container
