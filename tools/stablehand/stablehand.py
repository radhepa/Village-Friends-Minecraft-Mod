"""Stablehand's generated files: breed and gear tables, language names, art, recipes, trades and tags.

    python tools/stablehand/stablehand.py                    # write every module's files
    python tools/stablehand/stablehand.py --check            # exit 1 listing stale files or unknown vanilla ids
    python tools/stablehand/stablehand.py --preview          # preview sheets in build/previews/
    python tools/stablehand/stablehand.py --only breeds,gear # just these modules (with any of the above)
    python tools/stablehand/stablehand.py --vanilla-items    # refresh vanilla_items.txt from the 26.3 client jar

Each module (`MODULES`) has `outputs() -> {Path: bytes}` and `preview()`. A path written by two modules is
an error. `--check` compares PNGs byte for byte and text with line endings normalised, and fails on any
`minecraft:` item in a Stablehand recipe or stablehand trade that 26.3 does not have (vanilla_items.txt is
the snapshot; tags such as `#minecraft:dyes` are not item ids and are skipped).

Never hand-edit an output; change the module and rerun.
"""
import importlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kit import DATA, PROJECT  # noqa: E402

MODULES = ['lang', 'breeds', 'gear', 'yard', 'riders']
HERE = Path(__file__).resolve().parent
VANILLA_ITEMS = HERE / 'vanilla_items.txt'
CLIENT_JAR = Path.home() / '.gradle/caches/fabric-loom/26.3/minecraft-client.jar'
# Where vanilla ids are checked: Stablehand recipes and the stablehand's trades.
CHECKED = [DATA / 'villagefriends/recipe', DATA / 'villagefriends/villager_trade/stablehand']
# Fields whose strings are item ids, and subtrees that never hold one.
ITEM_FIELDS = {'id', 'item', 'items', 'key', 'ingredient', 'ingredients', 'base', 'addition', 'template', 'target'}
SKIPPED = {'components', 'type', 'merchant_predicate', 'predicate', 'predicates', 'conditions', 'fabric:load_conditions'}


def selected():
    for i, arg in enumerate(sys.argv):
        if arg == '--only' and i + 1 < len(sys.argv):
            names = [n.strip() for n in sys.argv[i + 1].split(',') if n.strip()]
            unknown = [n for n in names if n not in MODULES]
            if unknown:
                sys.exit(f'Unknown module(s) {unknown}; choose from {MODULES}')
            return names
    return MODULES


def outputs(names):
    files, owner = {}, {}
    for name in names:
        for path, data in importlib.import_module(name).outputs().items():
            path = Path(path)
            if path in files:
                sys.exit(f'{path.relative_to(PROJECT)} is written by both {owner[path]} and {name}')
            files[path], owner[path] = data, name
    return files


def same(path, data):
    if not path.exists():
        return False
    current = path.read_bytes()
    return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data.replace(b'\r\n', b'\n')


def item_ids(node, inside=False):
    """Every string under an item field of a recipe or trade, skipping components, types and predicates."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key not in SKIPPED:
                yield from item_ids(value, inside or key in ITEM_FIELDS)
    elif isinstance(node, list):
        for value in node:
            yield from item_ids(value, inside)
    elif isinstance(node, str) and inside:
        yield node


def unknown_vanilla(files):
    if not VANILLA_ITEMS.exists():
        return ['tools/stablehand/vanilla_items.txt is missing (run with --vanilla-items)']
    known = set(VANILLA_ITEMS.read_text(encoding='utf-8').split())
    bad = []
    for path, data in files.items():
        if path.suffix != '.json' or not any(path.is_relative_to(root) for root in CHECKED):
            continue
        for item in item_ids(json.loads(data.decode('utf-8'))):
            if item.startswith('minecraft:') and item[len('minecraft:'):] not in known:
                bad.append(f'{path.relative_to(PROJECT)}: {item}')
    return bad


def vanilla_items():
    with zipfile.ZipFile(CLIENT_JAR) as jar:
        names = sorted(Path(n).stem for n in jar.namelist() if n.startswith('assets/minecraft/items/') and n.endswith('.json'))
    VANILLA_ITEMS.write_text('\n'.join(names) + '\n', encoding='utf-8', newline='\n')
    print(f'{len(names)} vanilla items -> {VANILLA_ITEMS.relative_to(PROJECT)}')


def write(names):
    files, changed = outputs(names), 0
    for path, data in files.items():
        if same(path, data):
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        changed += 1
    print(f'Stablehand ({", ".join(names)}): {len(files)} files, {changed} written.')


def check(names):
    files = outputs(names)
    stale = [str(p.relative_to(PROJECT)) for p, data in files.items() if not same(p, data)]
    unknown = unknown_vanilla(files)
    if stale:
        print('Out of date (run tools/stablehand/stablehand.py):\n  ' + '\n  '.join(stale))
    if unknown:
        print('Not a 26.3 item:\n  ' + '\n  '.join(unknown))
    if stale or unknown:
        sys.exit(1)
    print(f'Stablehand ({", ".join(names)}): {len(files)} files up to date.')


def preview(names):
    for name in names:
        importlib.import_module(name).preview()


if __name__ == '__main__':
    if '--vanilla-items' in sys.argv:
        vanilla_items()
    elif '--check' in sys.argv:
        check(selected())
    elif '--preview' in sys.argv:
        preview(selected())
    else:
        write(selected())
