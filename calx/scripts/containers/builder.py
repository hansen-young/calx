import os
import hashlib
import tempfile
from pathlib import Path

import docker
from dirhash import dirhash, _get_filehash
from calx.dtypes import *
from calx.logger import default_logger as log


class DockerBuilder:
    @staticmethod
    def check_condition(args: Namespace, conf: Config) -> bool:
        return args.container == "docker"

    @staticmethod
    def create_dockerfile(args: Namespace, conf: Config) -> str:
        return (
            "FROM hansenyoung/calx:py3.7\n"
            "WORKDIR /usr/src/app\n"
            "RUN pip install git+https://github.com/haiyee99/calx.git@feature/containerize-runner\n"
            f"COPY {args.file} /tmp/calx-run/pipeline.yaml\n"
            f"COPY {args.workdir} .\n"
        )

    @staticmethod
    def get_version_hash(args: Namespace, conf: Config) -> str:
        hash_workdir = dirhash(args.workdir, "md5")
        hash_file = _get_filehash(args.file, hashlib.md5, chunk_size=1048576)

        final_hash = hashlib.md5(hash_workdir.encode("utf8"))
        final_hash.update(hash_file.encode("utf8"))

        return final_hash.hexdigest()

    @staticmethod
    def build(args: Namespace, conf: Config):
        name = conf["metadata"]["pipeline_name"].lower().replace("_", "-")
        version_hash = DockerBuilder.get_version_hash(args, conf)
        dockerfile = DockerBuilder.create_dockerfile(args, conf)

        client = docker.from_env()
        tag = f"calx-{name}:{version_hash}"
        os.environ["CALX_DOCKER_IMAGE_TAG"] = tag

        try:
            client.images.get(tag)
            log.info("found existing image, skip building...")

        except docker.errors.ImageNotFound:
            log.info("found new project version, building image...")

            with tempfile.TemporaryDirectory() as tmpdir:
                dockerfile_path = os.path.join(tmpdir, "Dockerfile")

                with open(dockerfile_path, "w") as fp:
                    fp.write(dockerfile)

                client.images.build(
                    tag=tag,
                    path=os.getcwd(),
                    dockerfile=dockerfile_path,
                    forcerm=True,
                )


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
