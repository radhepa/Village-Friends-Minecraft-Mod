"""Village type layouts: one main file per type plus optional fragments.

``tools/village_layouts/<type>.json`` describes one village type (its structure,
biomes, start pool, required civic pools, terrain survey and pools).
``tools/village_layouts/<type>.<part>.json`` fragments add more pools to that type,
so separate people can own, say, the lots without editing the main file.

Plains is the original village: its pools keep their historical names
(``town_centers``, ``buildings/tavern``, ``plains/streets``...) and its templates sit
at the top of ``tools/village_blueprints/``. Every other type namespaces its pools as
``<type>/...`` and its templates as ``<type>/<name>``.
"""
import json
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
LAYOUTS = TOOLS / 'village_layouts'
WORLD = TOOLS / 'village_world.json'
NS = 'villagefriends'
MAIN_KEYS = {'format', 'type', 'structure', 'villager_type', 'weight', 'biomes', 'start_pool', 'start_jigsaw', 'depth',
             'max_distance', 'terrain', 'prune', 'min_pieces', 'pools', 'required_pools', 'slot_widths',
             'processor_lists', 'terrain_adaptation'}
PART_KEYS = {'format', 'type', 'part', 'pools', 'processor_lists'}


def pool_spec(entries):
    """Pools are plain lists or objects with ``elements`` and a ``fallback``."""
    if isinstance(entries, list):
        return {'elements': entries, 'fallback': 'minecraft:empty'}
    return {'elements': entries['elements'], 'fallback': entries.get('fallback', 'minecraft:empty')}


def owns_pool(kind, pool):
    return kind == 'plains' or pool.startswith(kind + '/')


def owns_template(kind, template):
    return template == 'empty' or (('/' not in template) if kind == 'plains' else template.startswith(kind + '/'))


def load():
    """Return ``{type: layout}`` with fragments merged into their main layout."""
    mains, parts = {}, []
    for path in sorted(LAYOUTS.glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        assert data.get('format') == 3, f'{path.name}: layouts use format 3'
        stem = path.stem.split('.')
        kind = data['type']
        assert stem[0] == kind, f'{path.name}: file name must start with its type {kind!r}'
        if len(stem) == 1:
            unknown = set(data) - MAIN_KEYS
            assert not unknown, f'{path.name}: unknown keys {sorted(unknown)}'
            data['_files'] = [path.name]
            mains[kind] = data
        else:
            unknown = set(data) - PART_KEYS
            assert not unknown, f'{path.name}: fragments only add pools and processor lists, not {sorted(unknown)}'
            data['_file'] = path.name
            parts.append(data)
    for part in parts:
        kind = part['type']
        target = mains.setdefault(kind, {'type': kind, 'pools': {}, 'processor_lists': {}, '_files': [], '_detached': True})
        target['_files'].append(part['_file'])
        for name, spec in part.get('pools', {}).items():
            assert name not in target['pools'], f'{part["_file"]}: pool {name} is already defined for {kind}'
            target['pools'][name] = spec
        lists = target.setdefault('processor_lists', {})
        for name, spec in part.get('processor_lists', {}).items():
            assert name not in lists or lists[name] == spec, f'{part["_file"]}: processor list {name} differs'
            lists[name] = spec
    for kind, layout in mains.items():
        for name, spec in layout['pools'].items():
            layout['pools'][name] = pool_spec(spec)
            assert owns_pool(kind, name), f'{kind}: pool {name} must be named {kind}/...'
    return mains


def world():
    return json.loads(WORLD.read_text(encoding='utf-8'))


def structure_id(layout):
    return f'{NS}:{layout["structure"]}'


def pool_id(name):
    return name if ':' in name else f'{NS}:village/{name}'


def short_pool(name):
    return name.split(f'{NS}:village/')[-1]
