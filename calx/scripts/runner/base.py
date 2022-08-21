from calx.utils import read_environ


class BaseRunner:
    def __init__(self, name: str, envfile: str):
        self.name = name
        self.envfile = envfile
        self.envlist = read_environ(envfile)
