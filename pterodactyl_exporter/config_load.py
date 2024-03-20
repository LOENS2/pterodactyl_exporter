from yaml import load
from .dto.config import Config

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def get_config(path: str) -> Config:
    with open(path) as f:
        config_dict = load(f, Loader=Loader)
        return Config(**config_dict)
