import os
import sys
import time


class Debugger:
    def __init__(self):
        pass

    def _print_env(self):
        print("[ Environment Variables ]")
        for k, v in os.environ.items():
            print(f"{k}={v}")
        print()

    def _print_syspath(self):
        print("[ System Paths ]")
        for p in sys.path:
            print(f"- {p}")
        print()

    def _print_process_detail(self):
        print("[ Process Detail ]")
        print(f"pid: {os.getpid()}")
        print(f"cwd: {os.getcwd()}")
        print()

    def __call__(self):
        self._print_env()
        self._print_syspath()
        self._print_process_detail()


class Sleep:
    def __init__(self, time):
        self.time = time
        self.prefix = f"pid[{os.getpid()}]"

    def print(self, message: str):
        print(self.prefix, message)

    def __call__(self):
        self.print(f"sleep for {self.time}s")
        for i in range(self.time):
            self.print(f"{i+1}...")
            time.sleep(1)
