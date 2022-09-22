import argparse
from typing import Union, Callable
from omegaconf import ListConfig, DictConfig
from networkx import DiGraph


Config = Union[ListConfig, DictConfig]
Namespace = argparse.Namespace
