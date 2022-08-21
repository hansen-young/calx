import networkx as nx
from calx.dtypes import *
from calx.utils.file_reader import read_file, read_environ


def import_module(path: str):
    parse = path.split(".")
    module_path = ".".join(parse[:-1])
    classname = parse[-1]

    module = __import__(module_path, fromlist=["*"])
    return getattr(module, classname)


def construct_graph(nodes: list) -> DiGraph:
    graph = nx.DiGraph()

    for node in nodes:
        graph.add_node(node["name"])

        for dep in node["dependencies"]:
            graph.add_edge(dep, node["name"])

    return graph
