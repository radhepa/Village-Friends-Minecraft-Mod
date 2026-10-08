"""Registry of every design. Each module in ``buildings/`` exposes ``DESIGNS``.

Plains designs live directly in ``buildings/``. Each other village type has its own
package, ``buildings/<type>/``, whose design names all start with ``<type>/``.
"""
import importlib
import pkgutil

from . import buildings


def designs():
    found = {}
    for info in sorted(pkgutil.walk_packages(buildings.__path__, buildings.__name__ + '.'), key=lambda i: i.name):
        if info.ispkg:
            continue
        module = importlib.import_module(info.name)
        relative = info.name[len(buildings.__name__) + 1:].split('.')
        source = 'tools/village_design/buildings/' + '/'.join(relative) + '.py'
        package = relative[:-1]
        for name, build in getattr(module, 'DESIGNS', {}).items():
            assert name not in found, f'Duplicate design name {name}'
            if package:
                assert name.startswith(package[0] + '/'), f'{source}: {package[0]} designs are named {package[0]}/...'
            else:
                assert '/' not in name, f'{source}: plains designs have plain names'
            found[name] = (source, build)
    return found
