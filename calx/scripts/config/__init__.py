import os
import yaml
import pkg_resources
from omegaconf import OmegaConf

from calx import __version__
from calx.dtypes import *

__all__ = ["base_template", "base_template_from_args"]
__p_template = pkg_resources.resource_filename(__name__, "template")


def _read_template(filepath: str):
    with open(filepath, "r") as fp:
        return yaml.safe_load(fp)


def _read_base_template() -> dict:
    filepath = os.path.join(__p_template, "base.yaml")
    return _read_template(filepath)


def _read_backend_template(name: str) -> dict:
    name = name.lower()
    filepath = os.path.join(__p_template, f"tracking_{name}.yaml")

    if name == "none":
        return {}

    if not os.path.isfile(filepath):
        raise ValueError(f"Invalid tracking server: {name}")

    return _read_template(filepath)


def base_template(name: str, backend: str = "none") -> dict:
    conf = _read_base_template()
    conf["metadata"]["pipeline_name"] = name
    conf["metadata"]["sdk_version"] = __version__

    conf["tracking_server"]["backend"] = backend
    conf["tracking_server"]["options"] = _read_backend_template(backend)

    return conf


def base_template_from_args(args: Namespace) -> dict:
    """
    args should contain the following attributes:
    - name: str
    - backend: str
    """

    return base_template(
        args.name,
        args.backend,
    )


def _load_default_steps(conf: Config):
    if "steps" not in conf:
        conf["steps"] = DictConfig({})

    if "steps_dir" not in conf:
        return

    _supported_ext = (".yml", ".yaml")

    basepath = conf["steps_dir"]
    files = os.listdir(basepath)

    for file in files:
        ext = os.path.splitext(file)[-1].lower()

        if ext not in _supported_ext:
            continue

        fullpath = os.path.join(basepath, file)
        step_conf = OmegaConf.load(fullpath)

        if not isinstance(step_conf, DictConfig):
            raise ValueError(
                f"error processing '{file}': top-most level must be a dictionary."
            )

        for k, v in step_conf.items():
            if k not in conf["steps"]:
                conf["steps"][k] = v


def load_config(path: str) -> Config:
    conf = OmegaConf.load(path)
    _load_default_steps(conf)

    return conf


# ====== Environ ===== #
from dotenv import dotenv_values


def read_environ(file: str, workdir: str = None) -> dict:
    if not workdir:
        workdir = os.getcwd()

    if not file:
        return {}

    workdir = os.path.abspath(workdir)
    fullpath = os.path.join(workdir, file)

    if not os.path.isfile(fullpath):
        raise FileNotFoundError(f"environment file {fullpath} is missing.")

    return dotenv_values(fullpath)
