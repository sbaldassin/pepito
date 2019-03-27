import os
from configparser import ConfigParser
from os.path import abspath, dirname


def get_config():
    env = os.getenv("ARETO_ENV")
    if not env:
        env = "QA"

    config = ConfigParser()
    config_dir = abspath(dirname(__file__))
    config.read(os.path.join(config_dir, "{}.cfg".format(env.upper())))
    return config
