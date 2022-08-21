import argparse
from typing import Union
from omegaconf import ListConfig, DictConfig
from networkx import DiGraph


Config = Union[ListConfig, DictConfig]
Namespace = argparse.Namespace
