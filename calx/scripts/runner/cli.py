import subprocess
from calx.scripts.runner.base import BaseRunner


class CLIRunner(BaseRunner):
    def __init__(self, name: str, envfile: str):
        super().__init__(name, envfile)

    def __call__(self, command: str):
        # There is a security concern regarding the use of shell=True defined in
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        # however calx CLIRunner is made for running any shell command defined via
        # pipeline.yaml file. It is the users' responsibility to make sure that the
        # command is safe to run.
        subprocess.run(command, shell=True, capture_output=False, check=True)
