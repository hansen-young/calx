import argparse
from omegaconf import OmegaConf

from calx.dtypes import *
from calx.scripts.config import load_config
from calx.scripts.runner import ModuleRunner, CLIRunner, DockerRunner


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
    __runner = {
        "module": ModuleRunner,
        "cli": CLIRunner,
        "docker": DockerRunner,
    }

    step_conf = conf["steps"][step_name]
    step_type = step_conf["type"]
    step_options = step_conf["options"]
    step_envfile = step_conf.get("envfile")

    runner = __runner[step_type](name=step_name, envfile=step_envfile)
    runner(**step_options)


if __name__ == "__main__":
    args = parse_arguments()
    conf = load_config(args.file)

    run(args.step, conf)
