"""Compile every village type's blueprints and layout into Minecraft data.

Reads ``tools/village_blueprints/**`` and ``tools/village_layouts/*.json`` (see
``village_design/layouts.py``) and writes native, compressed templates, template
pools, processor lists, one ``villagefriends:village`` structure per type, their
biome tags, the ``minecraft:villages`` structure set that replaces the vanilla
villages, and the structure catalog the tests read.

Only Python's standard library is required. Rooms, beds and connectors are checked
before writing; the catalog also gives the later bed scanner reproducible fixtures.
Run: python tools/create_village_structures.py
"""
from collections import deque
from pathlib import Path
import gzip
import json
import struct
import argparse
import sys

ROOT = Path(__file__).resolve().parent.parent / 'src/main/resources'
NS = 'villagefriends'
DATA_VERSION = 5023  # The project's Minecraft 26.3 world format.
BLUEPRINTS = Path(__file__).resolve().parent / 'village_blueprints'
sys.path.insert(0, str(Path(__file__).resolve().parent))
from village_design import layouts as village_layouts  # noqa: E402


class Byte(int):
    pass


def tag_type(value):
    if isinstance(value, (Byte, bool)): return 1
    if isinstance(value, int): return 3
    if isinstance(value, float): return 6
    if isinstance(value, str): return 8
    if isinstance(value, list): return 9
    if isinstance(value, dict): return 10
    raise TypeError(value)


def string(value):
    encoded = value.encode('utf-8')
    return struct.pack('>H', len(encoded)) + encoded


def payload(value):
    kind = tag_type(value)
    if kind == 1: return struct.pack('>b', value)
    if kind == 3: return struct.pack('>i', value)
    if kind == 6: return struct.pack('>d', value)
    if kind == 8: return string(value)
    if kind == 9:
        element_type = tag_type(value[0]) if value else 10
        assert all(tag_type(v) == element_type for v in value)
        return bytes([element_type]) + struct.pack('>i', len(value)) + b''.join(payload(v) for v in value)
    return b''.join(bytes([tag_type(v)]) + string(k) + payload(v) for k, v in value.items()) + b'\0'


def write_json(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def state(name, **properties):
    result = {'Name': name if ':' in name else 'minecraft:' + name}
    if properties: result['Properties'] = {k: str(v).lower() for k, v in properties.items()}
    return result


class Template:
    def __init__(self, name, size):
        self.name, self.size = name, size
        self.blocks, self.nbt, self.entities = {}, {}, []
        self.rooms, self.doors, self.beds, self.connectors = [], [], [], []
        # Real air, rather than structure_void, clears foliage out of rooms.
        self.fill((0, 0, 0), tuple(v-1 for v in size), 'air')

    def put(self, x, y, z, name, nbt=None, **properties):
        assert all(0 <= p < limit for p, limit in zip((x, y, z), self.size)), (self.name, x, y, z)
        pos = (x, y, z)
        self.blocks[pos] = state(name, **properties)
        self.nbt.pop(pos, None)
        if nbt is not None: self.nbt[pos] = nbt

    def fill(self, low, high, name, **properties):
        for y in range(low[1], high[1]+1):
            for z in range(low[2], high[2]+1):
                for x in range(low[0], high[0]+1): self.put(x, y, z, name, **properties)

    def custom(self, x, y, z, name, facing='north'):
        entity = name in {'house_plaque', 'notice_board', 'command_desk', 'apothecary_cot'}
        self.put(x, y, z, NS+':'+name, {'id': NS+':'+name} if entity else None, facing=facing)

    def door(self, x, z, facing='north'):
        for y, half in [(1, 'lower'), (2, 'upper')]:
            self.put(x, y, z, 'oak_door', facing=facing, half=half, hinge='left', open=False, powered=False)
        self.doors.append([x, 1, z])

    def bed(self, x, y, z, color='red', facing='north'):
        dx, dz = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}[facing]
        for bx, bz, part in [(x, z, 'foot'), (x+dx, z+dz, 'head')]:
            self.put(bx, y, bz, color+'_bed', {'id': 'minecraft:bed'}, facing=facing, occupied=False, part=part)
        self.beds.append([x, y, z])

    def resident(self, x, y, z, job='none', child=False):
        profession = 'minecraft:none' if job == 'none' else NS+':'+job
        self.entities.append({'pos': [x+.5, float(y), z+.5], 'blockPos': [x, y, z], 'nbt': {
            'id': 'minecraft:villager', 'PersistenceRequired': Byte(1), 'Age': -24000 if child else 0,
            'VillagerData': {'type': 'minecraft:plains', 'profession': profession, 'level': 1},
            'Xp': 1 if job != 'none' else 0,
        }})

    def jigsaw(self, x, y, z, direction, name, target='unused', pool='minecraft:empty', final='minecraft:air'):
        name, target = NS+':'+name, NS+':'+target
        self.put(x, y, z, 'jigsaw', {'id': 'minecraft:jigsaw', 'name': name, 'target': target,
            'pool': pool, 'final_state': final, 'joint': 'aligned', 'selection_priority': 0,
            'placement_priority': 0}, orientation=direction+'_up')
        self.connectors.append({'pos': [x, y, z], 'direction': direction, 'name': name, 'target': target, 'pool': pool})

    def room(self, label, low, high):
        self.rooms.append({'name': label, 'min': list(low), 'max': list(high), 'probe': list(low)})

    def lantern_post(self, x, z, height=3):
        self.fill((x, 1, z), (x, height, z), 'oak_fence')
        self.put(x, height+1, z, 'lantern', hanging=False)

    def blueprint(self):
        """Human/LLM-editable layers; each character is one native block state."""
        symbols = '.' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,-/:;<=>?@[]^_{|}~'
        keys = {json.dumps(state('air'),sort_keys=True): '.'}
        palette = {'.': {'id': 'minecraft:air'}}
        for block in self.blocks.values():
            key = json.dumps(block, sort_keys=True)
            if key in keys: continue
            symbol = '.' if block['Name'] == 'minecraft:air' else symbols[len(keys)]
            keys[key] = symbol
            palette[symbol] = {'id': block['Name']}
            if 'Properties' in block: palette[symbol]['properties'] = block['Properties']
        def plain(value):
            if isinstance(value, Byte): return bool(value)
            if isinstance(value, dict): return {k: plain(v) for k,v in value.items()}
            if isinstance(value, list): return [plain(v) for v in value]
            return value
        return {'format': 1, 'size': list(self.size), 'palette': palette,
            'layers': [{'y': y, 'rows': [''.join(keys[json.dumps(self.blocks[(x,y,z)],sort_keys=True)]
                for x in range(self.size[0])) for z in range(self.size[2])]} for y in range(self.size[1])],
            'block_entities': [{'pos': list(p), 'nbt': plain(nbt)} for p,nbt in self.nbt.items()],
            'entities': plain(self.entities), 'rooms': self.rooms}

    @staticmethod
    def from_blueprint(path, name=None):
        data = json.loads(path.read_text(encoding='utf-8'))
        assert data['format'] == 1, f'Unsupported blueprint format: {path}'
        t = Template(name or path.stem, tuple(data['size']))
        assert len(data['layers']) == t.size[1], f'Include every Y layer: {path}'
        assert {layer['y'] for layer in data['layers']} == set(range(t.size[1])), f'Duplicate or missing Y layer: {path}'
        for layer in data['layers']:
            assert len(layer['rows']) == t.size[2], f'Wrong row count at Y={layer["y"]}: {path}'
            for z,row in enumerate(layer['rows']):
                assert len(row) == t.size[0], f'Wrong row width at Y={layer["y"]}, Z={z}: {path}'
                for x,symbol in enumerate(row):
                    block = data['palette'][symbol]
                    if block['id'] == 'minecraft:structure_void':
                        t.blocks.pop((x,layer['y'],z), None)  # Keep the world's block here.
                        continue
                    t.put(x,layer['y'],z,block['id'],**block.get('properties',{}))
        for entry in data['block_entities']:
            p = tuple(entry['pos'])
            assert p in t.blocks and t.blocks[p]['Name'] != 'minecraft:air', f'Block entity needs a block at {p}: {path}'
            t.nbt[p] = entry['nbt']
        t.entities = data['entities']
        for entity in t.entities:
            entity['pos'] = [float(v) for v in entity['pos']]
        t.rooms = data['rooms']
        for p,block in t.blocks.items():
            properties = block.get('Properties',{})
            if block['Name'].endswith('_bed') and properties.get('part') == 'foot': t.beds.append(list(p))
            if block['Name'].endswith('_door') and properties.get('half') == 'lower': t.doors.append(list(p))
            if block['Name'] == 'minecraft:jigsaw':
                nbt = t.nbt[p]
                t.connectors.append({'pos':list(p),'direction':properties['orientation'].split('_')[0],
                    'name':nbt['name'],'target':nbt['target'],'pool':nbt['pool']})
        return t

    def validate(self):
        for room in self.rooms:
            lo, hi = room['min'], room['max']
            # The future scanner can close doors conceptually and walk the air at
            # head height. Every partition, window, floor and ceiling is sealed.
            start = room.get('probe', lo)
            probe = (start[0], start[1]+1, start[2])
            def open_cell(pos):
                s = self.blocks.get(pos)
                if s is None: return True
                name = s['Name']
                return name == 'minecraft:air' or name in {
                    'minecraft:lantern', 'minecraft:wall_torch', 'minecraft:torch',
                    'minecraft:ladder', 'minecraft:flower_pot', 'minecraft:potted_fern',
                    'minecraft:potted_poppy', 'minecraft:potted_dandelion',
                } or (name.startswith(NS+':') and name != NS+':house_plaque')
            assert open_cell(probe), (self.name, room['name'], 'probe occupied')
            queue, seen = deque([probe]), {probe}
            while queue:
                x, y, z = queue.popleft()
                assert all(0 < v < limit-1 for v, limit in zip((x, y, z), self.size)), (self.name, room['name'], 'room escapes template')
                assert lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2], (self.name, room['name'], 'room connects across partition', x, z)
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    p = (x+dx, y+dy, z+dz)
                    if p not in seen and open_cell(p): seen.add(p); queue.append(p)
            count = sum(tuple(b) in seen or (b[0], b[1]+1, b[2]) in seen for b in self.beds)
            room['beds'] = count
            assert count > 0, (self.name, room['name'], 'room has no bed')
        for foot in self.beds:
            s = self.blocks[tuple(foot)]
            dx, dz = {'north': (0,-1), 'south': (0,1), 'east': (1,0), 'west': (-1,0)}[s['Properties']['facing']]
            head = self.blocks[(foot[0]+dx, foot[1], foot[2]+dz)]
            assert head['Properties']['part'] == 'head' and head['Name'] == s['Name'] and head['Properties']['facing'] == s['Properties']['facing']
        for x,y,z in self.doors:
            lower, upper = self.blocks[(x,y,z)], self.blocks[(x,y+1,z)]
            assert lower['Name'] == upper['Name'] and upper['Properties']['half'] == 'upper', (self.name,'door halves differ')
            assert {k:v for k,v in lower['Properties'].items() if k != 'half'} == {k:v for k,v in upper['Properties'].items() if k != 'half'}, (self.name,'door states differ')

    def save(self, write=True, villager_type='minecraft:plains'):
        self.validate()
        for entity in self.entities:
            if entity['nbt'].get('id') == 'minecraft:villager':
                entity['nbt']['VillagerData']['type'] = villager_type
        palette, indices, blocks = [], {}, []
        for pos, block in sorted(self.blocks.items(), key=lambda p: (p[0][1], p[0][2], p[0][0])):
            key = json.dumps(block, sort_keys=True)
            if key not in indices:
                indices[key] = len(palette)
                # 26.3 uses lower-case block-state fields in its current NBT format.
                encoded = {'id': block['Name']}
                if 'Properties' in block: encoded['properties'] = block['Properties']
                palette.append(encoded)
            entry = {'pos': list(pos), 'state': indices[key]}
            if pos in self.nbt: entry['nbt'] = self.nbt[pos]
            blocks.append(entry)
        data = {'DataVersion': DATA_VERSION, 'size': list(self.size), 'palette': palette,
                'blocks': blocks, 'entities': self.entities}
        target = ROOT / f'data/{NS}/structure/village/{self.name}.nbt'
        target.parent.mkdir(parents=True, exist_ok=True)
        if write:
            packed = gzip.compress(b'\x0a\x00\x00' + payload(data), mtime=0)
            # Pin the gzip OS byte so templates are byte-identical on every platform.
            target.write_bytes(packed[:9] + b'\x03' + packed[10:])
        return {'id': f'{NS}:village/{self.name}', 'size': list(self.size), 'rooms': self.rooms,
                'doors': self.doors, 'bed_feet': self.beds, 'residents': len(self.entities),
                'connectors': self.connectors, 'anchors': [
                    {'id': s['Name'], 'pos': list(p)} for p, s in self.blocks.items() if s['Name'].startswith(NS+':')]}




def location(template):
    return template if ':' in template else f'{NS}:village/{template}'


pool_name = village_layouts.pool_id


def pool(name, spec):
    elements = []
    for entry in spec['elements']:
        if entry.get('template') == 'empty':
            elements.append({'weight': entry['weight'], 'element': {'element_type': 'minecraft:empty_pool_element'}})
            continue
        processors = entry.get('processors', 'village')
        elements.append({'weight': entry['weight'], 'element': {'element_type': 'minecraft:single_pool_element',
            'location': location(entry['template']), 'processors': processors if ':' in processors else f'{NS}:{processors}',
            'projection': entry.get('projection', 'rigid')}})
    fallback = spec['fallback']
    write_json(f'data/{NS}/worldgen/template_pool/village/{name}.json',
               {'fallback': fallback if fallback == 'minecraft:empty' else pool_name(fallback), 'elements': elements})


def check_lot(t):
    """The drop-in contract for anything that attaches to a street or plaza slot."""
    entrance = [c for c in t.connectors if c['name'] == f'{NS}:building_entrance']
    assert len(entrance) == 1, f'{t.name}: lots need exactly one building_entrance jigsaw'
    pos = entrance[0]['pos']
    assert pos[1] == 1 and pos[2] == 0 and entrance[0]['direction'] == 'north', f'{t.name}: keep the north-facing building_entrance at [x,1,0]'
    nbt = t.nbt[tuple(pos)]
    assert nbt['pool'] == 'minecraft:empty' and nbt['final_state'] == 'minecraft:air', f'{t.name}: entrance must terminate with air'
    assert t.blocks[tuple(pos)]['Properties']['orientation'] == 'north_up' and nbt['joint'] == 'aligned', f'{t.name}: entrance orientation/joint must be north_up/aligned'
    assert 3 <= t.size[0] <= 32 and 3 <= t.size[2] <= 32 and 3 <= t.size[1] <= 32, f'{t.name}: lots are 3..32 blocks in each dimension'


def remove_stale(folder, keep, pattern='*.json'):
    if not folder.exists():
        return
    for stale in folder.rglob(pattern):
        if stale.relative_to(folder).as_posix() not in keep:
            stale.unlink()
    for sub in sorted(folder.rglob('*'), reverse=True):
        if sub.is_dir() and not any(sub.iterdir()):
            sub.rmdir()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', metavar='BUILDING', help='Write only this template plus the room catalog; keep other templates and pools unchanged.')
    parser.add_argument('--check', action='store_true', help='Validate blueprints and layouts without changing files.')
    args = parser.parse_args()
    layouts = village_layouts.load()
    assert 'plains' in layouts and not layouts['plains'].get('_detached'), 'The plains layout is required'
    templates = [Template.from_blueprint(p, p.relative_to(BLUEPRINTS).with_suffix('').as_posix())
                 for p in sorted(BLUEPRINTS.rglob('*.json'))]
    names = {t.name for t in templates}
    by_name = {t.name: t for t in templates}
    if args.only and args.only not in names: parser.error(f'Unknown blueprint: {args.only}')
    pools, owner, lists = {}, {}, {'village': []}
    for kind, layout in layouts.items():
        for name, spec in layout['pools'].items():
            assert name not in pools, f'Pool {name} is defined by both {owner.get(name)} and {kind}'
            pools[name], owner[name] = spec, kind
        for name, spec in layout.get('processor_lists', {}).items():
            assert name not in lists or lists[name] == spec, f'{kind}: processor list {name} differs from another type'
            lists[name] = spec
    used, kind_of = set(), {}
    for name, spec in pools.items():
        kind = owner[name]
        assert spec['elements'], f'Empty pool: {name}'
        fallback = spec['fallback']
        assert fallback == 'minecraft:empty' or (fallback in pools and owner[fallback] == kind), f'{name}: unknown fallback pool {fallback}'
        for entry in spec['elements']:
            assert 1 <= entry['weight'] <= 150, f'Invalid pool weight: {name}'
            if entry.get('template') == 'empty': continue
            template = entry['template']
            assert template in names, f'Pool {name} needs a blueprint for {template}'
            assert village_layouts.owns_template(kind, template), f'{name}: {kind} pools use {kind}/ templates, not {template}'
            assert entry.get('projection', 'rigid') in ('rigid', 'terrain_matching'), f'{name}: unknown projection'
            processors = entry.get('processors', 'village')
            assert ':' in processors or processors in lists, f'{name}: unknown processor list {processors}'
            assert kind_of.setdefault(template, kind) == kind, f'{template} is used by two village types'
            used.add(template)
            t = by_name[template]
            if any(c['name'] == f'{NS}:building_entrance' for c in t.connectors) or '/buildings/' in '/' + name:
                check_lot(t)
            for c in t.connectors:
                if c['pool'] != 'minecraft:empty':
                    target = village_layouts.short_pool(c['pool'])
                    assert target in pools, f'{t.name}: jigsaw at {c["pos"]} names unknown pool {c["pool"]}'
                    assert owner[target] == kind, f'{t.name}: a {kind} template may not reach the {owner[target]} pool {target}'
    unused = names - used
    assert not unused, f'Blueprints not referenced by any pool: {sorted(unused)}'
    populations = {t.name: len(t.entities) for t in templates}
    villages = []
    for kind, layout in sorted(layouts.items()):
        if layout.get('_detached'):
            continue
        # Civic slots around the square have fixed widths; a wider building would silently fail to place.
        for name, width in layout.get('slot_widths', {}).items():
            half = (width - 1) // 2
            for entry in pools[name]['elements']:
                if entry.get('template') == 'empty': continue
                t = by_name[entry['template']]
                ex = next(c['pos'][0] for c in t.connectors if c['name'] == f'{NS}:building_entrance')
                assert ex <= half and t.size[0] - 1 - ex <= half, f'{t.name}: {name} slots allow {half} blocks either side of the entrance'
        start = layout['start_pool']
        assert owner.get(start) == kind, f'{kind}: unknown start pool {start}'
        start_jigsaw = f'{NS}:{layout["start_jigsaw"]}'
        slot_pools = set()
        for entry in pools[start]['elements']:
            t = by_name[entry['template']]
            assert any(c['name'] == start_jigsaw for c in t.connectors), f'{t.name}: town centres need the {start_jigsaw} jigsaw'
            slot_pools |= {village_layouts.short_pool(c['pool']) for c in t.connectors if c['pool'] != 'minecraft:empty'}
        for name in layout['required_pools']:
            assert owner.get(name) == kind, f'{kind}: required pool {name} is missing'
        # The square and everything in its slots is never pruned for bad ground.
        keep = sorted({location(e['template']) for name in slot_pools | {start} for e in pools[name]['elements']
                       if e.get('template') != 'empty' and e.get('projection', 'rigid') == 'rigid'})
        horizontal = layout['max_distance'] if isinstance(layout['max_distance'], int) else layout['max_distance']['horizontal']
        villages.append({'type': kind, 'layout': layout, 'keep': keep, 'catalog': {
            'type': kind, 'structure': village_layouts.structure_id(layout), 'start_pool': pool_name(start),
            'start_jigsaw': start_jigsaw, 'min_pieces': layout['min_pieces'], 'depth': layout['depth'],
            'max_distance': horizontal, 'biomes': layout['biomes'],
            'required_modules': [{'pool': pool_name(name), 'templates': [location(e['template']) for e in pools[name]['elements'] if e.get('template') != 'empty']}
                                 for name in layout['required_pools']],
            'resident_minimum': sum(min(populations[e['template']] for e in pools[name]['elements'] if e.get('template') != 'empty')
                                    for name in layout['required_pools'])}})

    def villager_type(t):
        kind = kind_of[t.name]
        return layouts[kind].get('villager_type', 'minecraft:' + kind)

    catalog = {'templates': [t.save(write=not args.check and (not args.only or args.only == t.name), villager_type=villager_type(t))
                             for t in templates],
               'villages': [v['catalog'] for v in villages]}
    if args.check:
        print(f'Validated {len(templates)} independent blueprints, {len(pools)} pools and {len(villages)} village types; no files changed.')
        return
    write_json(f'data/{NS}/villagefriends/structure-catalog.json', catalog)
    if args.only:
        print(f'Updated {args.only}.nbt and room catalog; other templates and pools unchanged.')
        return
    remove_stale(ROOT / f'data/{NS}/structure/village', {f'{name}.nbt' for name in names}, '*.nbt')
    remove_stale(ROOT / f'data/{NS}/worldgen/template_pool/village', {f'{name}.json' for name in pools})
    for name, spec in pools.items(): pool(name, spec)
    for name, processors in lists.items():
        write_json(f'data/{NS}/worldgen/processor_list/{name}.json', {'processors': processors})
    structures = []
    for v in villages:
        layout, structure = v['layout'], v['layout']['structure']
        prune = dict(layout.get('prune', {}))
        prune['keep'] = v['keep']
        definition = {'type': f'{NS}:village', 'biomes': f'#{NS}:has_structure/{structure}', 'step': 'surface_structures',
            'spawn_overrides': {}, 'terrain_adaptation': layout.get('terrain_adaptation', 'beard_thin'),
            'start_pool': pool_name(layout['start_pool']), 'start_jigsaw_name': f'{NS}:{layout["start_jigsaw"]}',
            'size': layout['depth'], 'max_distance_from_center': layout['max_distance'], 'prune': prune}
        if 'terrain' in layout:
            definition['terrain'] = layout['terrain']
        write_json(f'data/{NS}/worldgen/structure/{structure}.json', definition)
        write_json(f'data/{NS}/tags/worldgen/biome/has_structure/{structure}.json', {'replace': False, 'values': layout['biomes']})
        structures.append({'structure': f'{NS}:{structure}', 'weight': layout.get('weight', 1)})
    written = {f'{v["layout"]["structure"]}.json' for v in villages}
    for folder in (ROOT / f'data/{NS}/worldgen/structure', ROOT / f'data/{NS}/tags/worldgen/biome/has_structure'):
        for stale in folder.glob('village*.json'):
            if stale.name not in written: stale.unlink()
    # Our types replace the vanilla villages under the vanilla set's name, so pillager
    # outposts and anything else that keeps its distance from villages still does.
    world = village_layouts.world()
    space, set_path = world['structure_set'].split(':')
    write_json(f'data/{space}/worldgen/structure_set/{set_path}.json', {'structures': structures, 'placement': world['placement']})
    legacy = ROOT / f'data/{NS}/worldgen/structure_set/villages.json'
    if legacy.exists(): legacy.unlink()
    target = ROOT / 'data/minecraft/tags/worldgen/structure/village.json'
    tag = json.loads(target.read_text()) if target.exists() else {'replace': False, 'values': []}
    ours = {s['structure'] for s in structures}
    tag['values'] = sorted({v for v in tag['values'] if not v.startswith(NS + ':')} | ours)
    write_json('data/minecraft/tags/worldgen/structure/village.json', tag)
    print(f'Generated {len(templates)} templates, {len(pools)} pools and {len(villages)} village types '
          f'({", ".join(v["type"] for v in villages)}) replacing the vanilla villages.')


if __name__ == '__main__': main()
