import os
import yaml
import pkg_resources

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
