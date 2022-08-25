import pytest

from mason_tools.parsers import parse_pyproject_toml

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
