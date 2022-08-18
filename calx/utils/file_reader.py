import os
import requests
from urllib.parse import urlparse, ParseResult


def _read_local_file(path: str) -> str:
    with open(path, "r") as fp:
        return fp.read()


def _read_file_from_link(path: str) -> str:
    with requests.get(path) as resp:
        return resp.text


def read_file(path: str) -> str:
    parsed = urlparse(path)

    if parsed.scheme in ("file", ""):
        return _read_local_file(path)

    return _read_file_from_link(path)


# ====== Environ ===== #
from dotenv import dotenv_values


def read_environ(file: str, basedir: str = None) -> dict:
    if not basedir:
        basedir = os.getcwd()

    if not file:
        return {}

    basedir = os.path.abspath(basedir)
    fullpath = os.path.join(basedir, file)

    if not os.path.isfile(fullpath):
        raise FileNotFoundError(f"environment file {fullpath} is missing.")

    return dotenv_values(fullpath)
