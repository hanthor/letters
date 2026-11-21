"""
Guards against the hand-copied constants in test_preferences.py drifting
from the code they mirror.

src/*.py imports gi/Adw and cannot be imported without a display stack, so
these tests read the real source with ``ast`` and compare it with the copies.
"""

import ast
from pathlib import Path

from test_preferences import FORMAT_MAP, STYLES_INT, STYLES_TAG

SRC = Path(__file__).resolve().parent.parent / "src"


def _tree(name):
    return ast.parse((SRC / name).read_text())


def _dict_assigned_in(tree, key_type):
    """Return every dict literal in *tree* whose keys are all ``key_type``
    constants, or ``_("...")`` calls when key_type is "gettext"."""
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict) or not node.keys:
            continue
        keys = []
        for k in node.keys:
            if key_type == "gettext" and isinstance(k, ast.Call) \
                    and getattr(k.func, "id", None) == "_" \
                    and isinstance(k.args[0], ast.Constant):
                keys.append(k.args[0].value)
            elif key_type == "str" and isinstance(k, ast.Constant) \
                    and isinstance(k.value, str):
                keys.append(k.value)
            else:
                break
        else:
            values = [ast.literal_eval(v) for v in node.values]
            found.append(dict(zip(keys, values)))
    return found


def test_format_map_matches_preferences_source():
    for node in _tree("preferences.py").body:
        if isinstance(node, ast.Assign) and \
                getattr(node.targets[0], "id", None) == "FORMAT_MAP":
            assert ast.literal_eval(node.value) == FORMAT_MAP
            return
    raise AssertionError("FORMAT_MAP not found in src/preferences.py")


def test_style_tag_map_matches_window_source():
    maps = _dict_assigned_in(_tree("window.py"), "gettext")
    assert STYLES_TAG in maps


def test_style_index_map_matches_window_source():
    maps = _dict_assigned_in(_tree("window.py"), "str")
    assert STYLES_INT in maps


def test_style_index_follows_dropdown_order():
    """The dropdown selects by position, so the index map must list the
    styles in the same order as the label map."""
    assert list(STYLES_INT) == list(STYLES_TAG.values())
