from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_config(path: str):
    with open(path) as f:
        return load(f, Loader=Loader)