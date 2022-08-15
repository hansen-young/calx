import argparse
from typing import Union
from omegaconf import ListConfig, DictConfig

from calx.scripts.runner.base import BaseRunner


Config = Union[ListConfig, DictConfig]
Namespace = argparse.Namespace
