from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def get_config(path: str):
    with open(path) as f:
        return load(f, Loader=Loader)