import os
import sys
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_config(path=None):
    if path is None:
        path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'default_config.yaml'
        )
    with open(path, "rb") as config_stream:
        data = load(config_stream, Loader=Loader)
        return data

storage_section = 'storage'