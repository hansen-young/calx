import os
import yaml
from collections import Counter

from calx.dtypes import *
from calx.utils import import_module
from calx.scripts.config import _read_template, __p_template


def _check_cycle_util(graph: dict, node: str, visited: dict):
    if visited[node] == 1:
        raise Exception("dag contains cycle")

    if visited[node] == 2:
        return

    visited[node] = 1

    for nx_node in graph[node]:
        _check_cycle_util(graph, nx_node, visited)

    visited[node] = 2


def _check_dag_has_cycle(conf: Config):
    graph = {node["name"]: node["dependencies"] for node in conf["dag"]}
    visited = {node["name"]: 0 for node in conf["dag"]}

    for node in graph:
        if visited[node] == 2:
            continue

        _check_cycle_util(graph, node, visited)


def _check_dag_correct_step(conf: Config):
    visited = set()
    names = {node["name"] for node in conf["dag"]}
    steps = {step for step in conf["steps"]}

    for node in conf["dag"]:
        # check if node name is defined multiple times
        if node["name"] in visited:
            raise KeyError(
                f"`node {node['name']}` is defined multiple times in dag",
            )

        visited.add(node["name"])

        # check if step name is valid
        if node["step"] not in steps:
            raise KeyError(
                f"unknown step `{node['step']}` in dag node `{node['name']}`",
            )

        # check if dependencies are valid node names
        for dep in node["dependencies"]:
            if dep not in names:
                raise KeyError(f"dependency `{dep}` is not defined in dag")


def _check_dag(conf: Config):
    _check_dag_correct_step(conf)
    _check_dag_has_cycle(conf)


def _check_steps_confkeys(conf: Config):
    __required_keys = {"type", "options"}
    __optional_keys = {"envfile"}

    for name, opt in conf["steps"].items():
        # Check if the required attributes exists
        for key in __required_keys:
            if key not in opt:
                raise KeyError(f"required attribute `{key}` in step `{name}`")

        # Check if step type is valid
        stype = opt["type"].lower()
        filepath = os.path.join(__p_template, f"schema_step_{stype}.yaml")

        if not os.path.isfile(filepath):
            raise ValueError(f"type `{stype}` is invalid in step `{name}`")

        # Check if step options is valid
        with open(filepath, "r") as fp:
            __required_opts = yaml.safe_load(fp)["required"]

        for tkey, tval in __required_opts.items():
            if tkey not in opt["options"]:
                raise KeyError(f"required option `{tkey}` in step `{name}`")


def _check_steps_type_module(opt: dict):
    klass = import_module(opt["path"])
    klass(**opt["arguments"])


def _check_steps(conf: Config):
    _check_steps_confkeys(conf)

    for step, opt in conf["steps"].items():
        if opt["type"].lower() == "module":
            _check_steps_type_module(opt["options"])


def check_pipeline_configs(conf: Config):
    _check_steps(conf)
    _check_dag(conf)
