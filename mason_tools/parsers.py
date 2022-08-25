from configparser import ConfigParser

import toml


def parse_pyproject_toml(content):
    try:
        return toml.loads(content)["build-system"]["requires"]
    except KeyError:
        return []


def parse_setup_cfg(content):
    config = ConfigParser()
    config.read_string(content)
    try:
        build_requirements = config["options"]["setup_requires"]
    except KeyError:
        return []

    return [req.strip() for req in build_requirements.strip().splitlines()]
