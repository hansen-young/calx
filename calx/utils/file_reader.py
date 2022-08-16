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
