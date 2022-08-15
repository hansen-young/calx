import time
import argparse
import multiprocessing as mp

from omegaconf import OmegaConf
from calx.dtypes import *
from calx.scripts.config.check import check_pipeline_configs
from calx.scripts.utils import _import_module
from calx.scripts.runner import ModuleRunner


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="run all steps defined in pipeline",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="pipeline.yaml",
        help="the path to pipeline.yaml file",
    )
    parser.add_argument(
        "-s",
        "--step",
        type=str,
        default=None,
        help="run single pipeline step",
    )
    parser.add_argument(
        "workdir",
        type=str,
        help="working directory",
    )

    return parser.parse_args()


def run_step(step: str, workdir: str, conf: Config) -> BaseRunner:
    step_conf = conf["steps"][step]
    stype = step_conf["type"].lower()

    if stype == "module":
        runner = ModuleRunner(
            **step_conf["options"],
            envlist={"MYTESTKEY": "VALUE"},
            workdir=workdir,
        )

    runner()
    return runner


def run_pipeline(workdir: str, conf: Config):
    running = {}
    queued = {}
    to_pop = []

    # prepare queue
    for c in conf["dag"]:
        queued[c["name"]] = {
            "step": c["step"],
            "dependencies": set(c["dependencies"]),
        }

    while len(queued) > 0:
        # move job from queue to running
        to_pop.clear()
        for name, c in queued.items():
            if not c["dependencies"]:
                running[name] = run_step(c["step"], workdir, conf)
                to_pop.append(name)

        for qname in to_pop:
            del queued[qname]

        # remove finished process
        to_pop.clear()
        while True:
            for pname in running:
                if running[pname].is_finished():
                    to_pop.append(pname)

            if to_pop:
                break

            time.sleep(0.5)

        for pname in to_pop:
            del running[pname]

            for qname in queued:
                queued[qname]["dependencies"].discard(pname)

    return


def run(args: Namespace, conf: Config):
    if args.all:
        _ = run_pipeline(args.workdir, conf)

    elif args.step:
        _ = run_step(args.step, args.workdir, conf)


def main():
    args = parse_arguments()
    conf = OmegaConf.load(args.file)

    # == !DEBUG! ==
    print("[calx-run]")
    print(vars(args))
    print(conf)
    # =============

    check_pipeline_configs(conf)
    run(args, conf)
