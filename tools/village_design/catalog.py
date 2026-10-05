"""Registry of every design. Each module in ``buildings/`` exposes ``DESIGNS``."""
import importlib
import pkgutil

from . import buildings


def designs():
    found = {}
    for info in sorted(pkgutil.iter_modules(buildings.__path__), key=lambda i: i.name):
        module = importlib.import_module(f'{buildings.__name__}.{info.name}')
        source = f'tools/village_design/buildings/{info.name}.py'
        for name, build in getattr(module, 'DESIGNS', {}).items():
            assert name not in found, f'Duplicate design name {name}'
            found[name] = (source, build)
    return found
