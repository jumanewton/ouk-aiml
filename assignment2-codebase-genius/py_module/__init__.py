"""Expose helper modules from the local py_modules directory as a package."""
import sys
from pathlib import Path

_package_dir = Path(__file__).resolve().parent
_root_dir = _package_dir.parent
_py_modules_dir = (_root_dir / "py_modules").resolve()

__path__ = [str(_package_dir)]

if _py_modules_dir.is_dir():
    if str(_root_dir) not in sys.path:
        sys.path.insert(0, str(_root_dir))
    if str(_py_modules_dir) not in sys.path:
        sys.path.insert(0, str(_py_modules_dir))
    __path__.append(str(_py_modules_dir))
