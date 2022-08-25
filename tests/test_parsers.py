import pytest

from mason_tools.parsers import parse_pyproject_toml, parse_setup_cfg, parse_setup_py

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


EXAMPLE_SETUP_PY = """
from setuptools import setup

setup()
"""

EXAMPLE_SETUP_PY_DIRECT = """
from setuptools import setup

setup(
    setup_requires=[
        "foo",  # comments should not be a problem
    ],
)
"""


EXAMPLE_SETUP_PY_CONSTANT = """
from setuptools import setup

SETUP_REQUIRES = [
    "bar",  # some comment
]

setup(
    setup_requires=SETUP_REQUIRES,
)
"""

EXAMPLE_SETUP_PY_NO_SETUP = """
def foo():
    ...
"""

EXAMPLE_SETUP_PY_INDIRECT = """
from setuptools import setup
DEP = "baz"
SETUP_REQUIRES = [DEP]
setup(setup_requires=SETUP_REQUIRES)
"""

EXAMPLE_SETUP_PY_IMPORTED = """
from setuptools import setup
from foo import bar
setup(setup_requires=bar)
"""

# next two are far fetch
EXAMPLE_SETUP_PY_KWARGS_DICT_CALL = """
from setuptools import setup

kwargs = dict(setup_requires="foo")
setup(**kwargs)
"""
EXAMPLE_SETUP_PY_KWARGS_DICT_LITERAL = """
from setuptools import setup

kwargs = {"setup_requires": "foo"}
setup(**kwargs)
"""


@pytest.mark.parametrize(
    "setup_py,expected_result",
    [
        (EXAMPLE_SETUP_PY, []),
        (EXAMPLE_SETUP_PY_CONSTANT, ["bar"]),
        (EXAMPLE_SETUP_PY_DIRECT, ["foo"]),
        (EXAMPLE_SETUP_PY_IMPORTED, []),
        (EXAMPLE_SETUP_PY_INDIRECT, ["baz"]),
        (EXAMPLE_SETUP_PY_NO_SETUP, []),
        pytest.param(
            EXAMPLE_SETUP_PY_KWARGS_DICT_CALL,
            ["foo"],
            marks=pytest.mark.xfail(reason="not implemented"),
        ),
        pytest.param(
            EXAMPLE_SETUP_PY_KWARGS_DICT_LITERAL,
            ["foo"],
            marks=pytest.mark.xfail(reason="not implemented"),
        ),
    ],
)
def test_parse_setup_py(setup_py, expected_result):
    assert parse_setup_py(setup_py) == expected_result
