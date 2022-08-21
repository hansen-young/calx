import subprocess


class CLIRunner:
    def __init__(self, command: str):
        self.command = command

    def __call__(self):
        # There is a security concern regarding the use of shell=True defined in
        # https://docs.python.org/3/library/subprocess.html#security-considerations
        # however calx CLIRunner is made for running any shell command defined via
        # pipeline.yaml file. It is the users' responsibility to make sure that the
        # command is safe to run.
        subprocess.run(self.command, shell=True, capture_output=False, check=True)
