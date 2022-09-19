import os
import yaml
import argparse

from calx.dtypes import *
from calx.logger import default_logger as log
from calx.scripts.config import base_template_from_args, __p_template


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="the pipeline name",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    # Create New Project Directory
    if os.path.isdir(args.name):
        raise FileExistsError(f"found existing project `{args.name}`.")

    os.mkdir(args.name)
    os.mkdir(os.path.join(args.name, "components"))
    os.mkdir(os.path.join(args.name, "tests"))
    open(os.path.join(args.name, ".env"), "w").close()

    # Create New Config Template
    config = base_template_from_args(args)
    config_path = os.path.join(args.name, "pipeline.yaml")

    with open(config_path, "w") as fp:
        yaml.dump(config, fp, sort_keys=False)
        log.info(f"created new file: {config_path}")
