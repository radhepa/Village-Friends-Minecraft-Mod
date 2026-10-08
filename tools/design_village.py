"""Write village blueprints from the Python designs in ``tools/village_design/``.

    python tools/design_village.py                 # every design
    python tools/design_village.py tavern cottage_oak
    python tools/design_village.py --list
    python tools/design_village.py --preview       # also writes isometric PNGs (needs Pillow)

Each design writes one independent ``tools/village_blueprints/<name>.json``
(other village types include their folder, e.g. ``desert/tavern``).
A blueprint records its design source and a checksum. If someone hand-edits
the JSON afterwards, this script leaves it alone unless ``--force`` is given,
so hand edits are never silently replaced. Then run
``python tools/create_village_structures.py`` to compile the NBT templates.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from village_design import catalog  # noqa: E402
from village_design.kit import checksum, dump  # noqa: E402

BLUEPRINTS = HERE / 'village_blueprints'


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('names', nargs='*', help='Design names (default: all).')
    parser.add_argument('--list', action='store_true', help='List designs and exit.')
    parser.add_argument('--force', action='store_true', help='Overwrite blueprints that were edited by hand.')
    parser.add_argument('--preview', action='store_true', help='Render isometric previews to build/previews.')
    args = parser.parse_args()
    designs = catalog.designs()
    if args.list:
        for name, (module, _) in sorted(designs.items()):
            print(f'{name:28s} {module}')
        return
    unknown = [n for n in args.names if n not in designs]
    if unknown:
        parser.error(f'Unknown design(s): {", ".join(unknown)}')
    written, skipped = [], []
    for name in args.names or sorted(designs):
        module, build = designs[name]
        b = build()
        assert b.name == name, f'{module}: design {name} built {b.name}'
        b.source = module
        data = b.finish().blueprint()
        target = BLUEPRINTS / f'{name}.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not args.force:
            old = json.loads(target.read_text(encoding='utf-8'))
            design = old.get('design')
            if not design or design.get('checksum') != checksum(old):
                skipped.append(name)
                continue
        target.write_text(dump(data), encoding='utf-8')
        written.append(name)
        if args.preview:
            from village_design import preview
            out = HERE.parent / 'build/previews'
            out.mkdir(parents=True, exist_ok=True)
            for view in ('nw', 'se'):
                preview.render(data, 12, view).save(out / f'{name.replace("/", "_")}_{view}.png')
    print(f'Wrote {len(written)} blueprint(s).')
    if skipped:
        print('Kept hand-edited blueprint(s) (use --force to replace): ' + ', '.join(skipped))


if __name__ == '__main__':
    main()
