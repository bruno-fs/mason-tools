import ast
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


def parse_setup_py(content):
    code_tree = ast.parse(content)
    setup_expr = _get_setup_expr(code_tree)
    if setup_expr is None:
        # module don't have a setup call
        return []

    deps_ast = _get_setup_requires(setup_expr, code_tree)
    return _resolve_deps(deps_ast, code_tree)


def _get_setup_expr(module: ast.Module) -> ast.Expr:
    for elem in module.body:
        if (
            isinstance(elem, ast.Expr)
            and isinstance(elem.value, ast.Call)
            and elem.value.func.id == "setup"
        ):
            return elem


def _get_setup_requires(setup_expr: ast.Expr, module: ast.Module):
    for kw in setup_expr.value.keywords:
        if kw.arg == "setup_requires":
            return kw.value


def _resolve_name(name: ast.Name, module: ast.Module):
    for elem in module.body:
        if isinstance(elem, ast.Assign):
            assert len(elem.targets) == 1, "Unsupported setup.py"
            assert isinstance(elem.targets[0], ast.Name), "Unsupported setup.py"
            if elem.targets[0].id == name.id:
                if isinstance(elem.value, ast.Name):
                    return _resolve_name(elem.value, module)
                return elem.value


def _value_getter(element, module: ast.Module):
    if isinstance(element, ast.Constant):
        return element.value
    elif isinstance(element, ast.Name):
        target_element = _resolve_name(element, module)
        return _value_getter(target_element, module)
    raise NotImplementedError()


def _resolve_deps(deps_ast, module: ast.Module):
    if deps_ast is None:
        return []
    if isinstance(deps_ast, ast.List):
        return [_value_getter(el, module) for el in deps_ast.elts]
    elif isinstance(deps_ast, ast.Name):
        value = _resolve_name(deps_ast, module)
        return _resolve_deps(value, module)
    raise NotImplementedError()
