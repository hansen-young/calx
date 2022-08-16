from calx.components.base import BaseComponent
from calx.components.retrieve_data.database import read_database_from_file
from omegaconf import OmegaConf

__valid_source = {"database", "cloudstorage", "file"}


def __check_constructor_options(name: str, source: str, opt: dict):
    if source not in __valid_source:
        raise ValueError(f"source `{source}` is not supported.")

    if source == "database":
        pass


class RetrieveData(BaseComponent):
    """
    data contains:
    - name: str
      source: str {database, cloudstorage, file}
      options:
        uri: str
        query_file: str
        query_param: dict
    """

    def __init__(self, data: list, **kwargs):
        self.data = data

    def __call__(self):
        print("Retrieve Data Module Called...")

        # == !DEBUG! ==
        for data in self.data:
            if data["source"] == "database":
                df = read_database_from_file(**data["options"])
                print(df)

            # OmegaConf.resolve(data)
            # print(type(data))
            # print(data, end="\n\n")
        # =============
