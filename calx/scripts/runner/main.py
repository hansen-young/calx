import argparse
from omegaconf import OmegaConf

from calx.dtypes import *
from calx.scripts.runner import ModuleRunner


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="the path to pipeline.yaml file",
    )
    parser.add_argument(
        "-s",
        "--step",
        type=str,
        required=True,
        help="step name to run",
    )

    return parser.parse_args()


def run(step_name: str, conf: Config):
    __runner = {"module": ModuleRunner}

    step_conf = conf["steps"][step_name]
    step_type = step_conf["type"]
    step_options = step_conf["options"]

    runner = __runner[step_type](**step_options)
    runner()


if __name__ == "__main__":
    args = parse_arguments()
    conf = OmegaConf.load(args.file)

    run(args.step, conf)
