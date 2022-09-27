from calx.dtypes import *
from calx.scripts.containers.core import BaseContainer, LocalContainer, DockerContainer


__containers = {
    "local": LocalContainer,
    "docker": DockerContainer,
}


def spawn_container(
    container_type: str,
    step_name: str,
    config_file: str,
    workdir: str,
    envlist: dict,
    output: str = None,
) -> BaseContainer:
    container = __containers[container_type]()
    container.run(
        step_name=step_name,
        config_file=config_file,
        workdir=workdir,
        envlist=envlist,
        output=output,
    )

    return container
