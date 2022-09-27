import os
from omegaconf import OmegaConf


def output_resolver(step: str):
    filepath = os.path.join(os.environ["CALX_TMPDIR"], step)

    with open(filepath, "r") as fp:
        return fp.read()


OmegaConf.register_new_resolver("output", output_resolver)
