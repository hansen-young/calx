import docker
from calx.dtypes import *


class DockerBuilder:
    @staticmethod
    def check_condition(args: Namespace, conf: Config) -> bool:
        if args.container == "docker":
            return True

        for name, step in conf["steps"].items():
            if step["type"] == "docker":
                return True

        return False

    @staticmethod
    def build(*args, **kwargs):
        client = docker.from_env()

        # ===== !NOT DONE! =====
        raise Exception("Implementation not done")


class LocalBuilder:
    @staticmethod
    def check_condition(args: Namespace, conf: Config) -> bool:
        return False

    @staticmethod
    def build(*args, **kwargs):
        pass


def build(args: Namespace, conf: Config):
    builders = (DockerBuilder, LocalBuilder)

    for builder in builders:
        if builder.check_condition(args, conf):
            builder.build(args, conf)
