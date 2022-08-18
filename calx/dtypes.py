import argparse
from typing import Union
from omegaconf import ListConfig, DictConfig


Config = Union[ListConfig, DictConfig]
Namespace = argparse.Namespace
