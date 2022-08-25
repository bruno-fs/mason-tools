import toml


def parse_pyproject_toml(content):
    try:
        return toml.loads(content)["build-system"]["requires"]
    except KeyError:
        return []
