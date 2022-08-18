from calx.utils.file_reader import read_file, read_environ


def import_module(path: str):
    parse = path.split(".")
    module_path = ".".join(parse[:-1])
    classname = parse[-1]

    module = __import__(module_path, fromlist=["*"])
    return getattr(module, classname)
