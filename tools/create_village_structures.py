"""Reproduce the Phase 2 village pools and native, compressed Minecraft templates.

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

ROOT = Path(__file__).resolve().parent.parent / 'src/main/resources'
NS = 'villagefriends'
DATA_VERSION = 5023  # The project's Minecraft 26.3 world format.
BLUEPRINTS = Path(__file__).resolve().parent / 'village_blueprints'
LAYOUT = Path(__file__).resolve().parent / 'village_layout.json'


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
    def from_blueprint(path):
        data = json.loads(path.read_text(encoding='utf-8'))
        assert data['format'] == 1, f'Unsupported blueprint format: {path}'
        t = Template(path.stem, tuple(data['size']))
        assert len(data['layers']) == t.size[1], f'Include every Y layer: {path}'
        assert {layer['y'] for layer in data['layers']} == set(range(t.size[1])), f'Duplicate or missing Y layer: {path}'
        for layer in data['layers']:
            assert len(layer['rows']) == t.size[2], f'Wrong row count at Y={layer["y"]}: {path}'
            for z,row in enumerate(layer['rows']):
                assert len(row) == t.size[0], f'Wrong row width at Y={layer["y"]}, Z={z}: {path}'
                for x,symbol in enumerate(row):
                    block = data['palette'][symbol]
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
            probe = (lo[0], lo[1]+1, lo[2])
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

    def save(self, write=True):
        self.validate()
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
        if write: target.write_bytes(gzip.compress(b'\x0a\x00\x00' + payload(data), mtime=0))
        return {'id': f'{NS}:village/{self.name}', 'size': list(self.size), 'rooms': self.rooms,
                'doors': self.doors, 'bed_feet': self.beds, 'residents': len(self.entities),
                'connectors': self.connectors, 'anchors': [
                    {'id': s['Name'], 'pos': list(p)} for p, s in self.blocks.items() if s['Name'].startswith(NS+':')]}


def location(template):
    return template if ':' in template else f'{NS}:village/{template}'


def pool(name, entries):
    write_json(f'data/{NS}/worldgen/template_pool/village/{name}.json', {'fallback':'minecraft:empty', 'elements':[
        {'weight':entry['weight'], 'element':{'element_type':'minecraft:single_pool_element',
         'location':location(entry['template']), 'processors':f'{NS}:village', 'projection':'rigid'}} for entry in entries]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', metavar='BUILDING', help='Write only this template plus the room catalog; keep other templates and pools unchanged.')
    parser.add_argument('--check', action='store_true', help='Validate blueprints and layout without changing files.')
    args = parser.parse_args()
    layout = json.loads(LAYOUT.read_text(encoding='utf-8'))
    assert layout['format'] == 1
    templates = [Template.from_blueprint(p) for p in sorted(BLUEPRINTS.glob('*.json'))]
    names = {t.name for t in templates}
    by_name = {t.name:t for t in templates}
    if args.only and args.only not in names: parser.error(f'Unknown blueprint: {args.only}')
    for name,entries in layout['pools'].items():
        assert entries, f'Empty pool: {name}'
        for entry in entries:
            assert entry['template'] in names, f'Pool {name} needs a blueprint for {entry["template"]}'
            assert 1 <= entry['weight'] <= 150, f'Invalid pool weight: {name}'
            if name.startswith('buildings/'):
                t = by_name[entry['template']]
                assert t.size[0] == 17 and t.size[2] == 19 and 3 <= t.size[1] <= 32, f'{t.name}: keep the 17x19 lot, with height 3..32'
                entrance = [c for c in t.connectors if c['name'] == f'{NS}:building_entrance']
                assert len(entrance) == 1 and entrance[0]['pos'] == [8,1,0] and entrance[0]['direction'] == 'north', f'{t.name}: keep the north-facing building_entrance at [8,1,0]'
                nbt = t.nbt[(8,1,0)]
                assert nbt['pool'] == 'minecraft:empty' and nbt['final_state'] == 'minecraft:air', f'{t.name}: entrance must terminate with air'
                assert t.blocks[(8,1,0)]['Properties']['orientation'] == 'north_up' and nbt['joint'] == 'aligned', f'{t.name}: entrance orientation/joint must be north_up/aligned'
    catalog = {'structure':f'{NS}:village','start_pool':layout['start_pool'],
        'start_jigsaw':layout['start_jigsaw'],'expected_pieces':layout['expected_pieces'],
        'templates':[t.save(write=not args.check and (not args.only or args.only==t.name)) for t in templates],
        'required_modules':[{'pool':f'{NS}:village/{name}', 'templates':[location(e['template']) for e in layout['pools'][name]]}
                            for name in layout['required_pools']]}
    populations = {t.name:len(t.entities) for t in templates}
    catalog['resident_range'] = [sum(op(populations[e['template']] for e in layout['pools'][name])
                                for name in layout['required_pools']) for op in (min,max)]
    if args.check:
        print(f'Validated {len(templates)} independent blueprints and {len(layout["pools"])} pools; no files changed.')
        return
    write_json(f'data/{NS}/villagefriends/structure-catalog.json',catalog)
    if args.only:
        print(f'Updated {args.only}.nbt and room catalog; other templates and pools unchanged.')
        return
    for name,entries in layout['pools'].items(): pool(name,entries)
    write_json(f'data/{NS}/worldgen/processor_list/village.json',{'processors':[]})
    write_json(f'data/{NS}/worldgen/structure/village.json',{
        'type':'minecraft:jigsaw', 'biomes':f'#{NS}:has_structure/village', 'step':'surface_structures',
        'spawn_overrides':{}, 'terrain_adaptation':'beard_thin', 'start_pool':catalog['start_pool'],
        'start_jigsaw_name':catalog['start_jigsaw'], 'size':layout['depth'], 'start_height':{'absolute':0},
        'project_start_to_heightmap':'WORLD_SURFACE_WG', 'max_distance_from_center':layout['max_distance'], 'use_expansion_hack':False})
    write_json(f'data/{NS}/worldgen/structure_set/villages.json',{'structures':[{'structure':catalog['structure'],'weight':1}],
        'placement':layout['placement']})
    write_json(f'data/{NS}/tags/worldgen/biome/has_structure/village.json',{'replace':False,'values':layout['biomes']})
    target = ROOT/'data/minecraft/tags/worldgen/structure/village.json'
    tag = json.loads(target.read_text()) if target.exists() else {'replace':False,'values':[]}
    tag['values'] = sorted(set(tag['values']) | {catalog['structure']})
    write_json('data/minecraft/tags/worldgen/structure/village.json',tag)
    print(f'Generated {len(templates)} templates, {len(layout["pools"])} pools, natural village placement and enclosed-room fixtures.')


if __name__ == '__main__': main()
