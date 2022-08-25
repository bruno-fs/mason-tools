import pytest

from mason_tools.parsers import parse_pyproject_toml, parse_setup_cfg

EXAMPLE_TOML = """
[build-system]
requires = [
    "foo", # some comment
    "bar", # more comments
]

[tool.black]
target-version = ["py310"]
"""

EXAMPLE_TOML_WO_BUILD_SYSTEM = """
[tool.black]
target-version = ["py310"]
"""


@pytest.mark.parametrize(
    "toml,expected_result",
    [(EXAMPLE_TOML, ["foo", "bar"]), (EXAMPLE_TOML_WO_BUILD_SYSTEM, [])],
)
def test_parse_toml(toml, expected_result):
    assert parse_pyproject_toml(toml) == expected_result


EXAMPLE_CFG = """
[metadata]
name = foo

[options]
# comments are not supported inside keywords
setup_requires =
    foo
    bar
"""

EXAMPLE_CFG_WO_SETUP_REQUIRES = """
[metadata]
name = foo

[options]
install_requires =
    foo
    bar
"""


@pytest.mark.parametrize(
    "setup_cfg,expected_result",
    [(EXAMPLE_CFG, ["foo", "bar"]), (EXAMPLE_CFG_WO_SETUP_REQUIRES, [])],
)
def test_parse_setup_cfg(setup_cfg, expected_result):
    assert parse_setup_cfg(setup_cfg) == expected_result
