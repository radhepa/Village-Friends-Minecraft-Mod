"""Core of the Village Friends design kit.

A ``Build`` is a sparse voxel canvas. Buildings are written as small Python
programs (see ``buildings/``) and exported to the layered blueprint JSON that
``tools/create_village_structures.py`` compiles into NBT templates.

Jigsaw templates are placed with a *known shape*: Minecraft keeps the block
states stored in the template instead of recomputing them from neighbours.
``Build.finish()`` therefore fills in the states the game would normally
derive -- fence/pane/wall connections, wall posts and stair corner shapes --
so the exported blueprint looks right in the world.

Coordinates are X east, Y up, Z south. Building fronts face north (Z=0).
"""
from collections import Counter, deque
import hashlib
import json
import re

NS = 'villagefriends'
DIRS = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}
OPPOSITE = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
CLOCKWISE = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
COUNTER = {v: k for k, v in CLOCKWISE.items()}
AXIS = {'north': 'z', 'south': 'z', 'east': 'x', 'west': 'x'}
AIR = ('minecraft:air', ())


# Blocks Minecraft renamed; designs may keep the familiar name.
RENAMED = {'chain': 'iron_chain'}


def full_id(name):
    name = RENAMED.get(name, name)
    return name if ':' in name else 'minecraft:' + name


def block(spec, **props):
    """``block('oak_stairs[facing=north]', half='top')`` -> canonical (id, props)."""
    if isinstance(spec, tuple):
        name, base = spec[0], dict(spec[1])
    else:
        match = re.fullmatch(r'([a-z0-9_:]+)(?:\[(.*)\])?', spec.strip())
        assert match, f'Bad block spec: {spec}'
        name, base = match.group(1), {}
        if match.group(2):
            for pair in match.group(2).split(','):
                key, value = pair.split('=')
                base[key.strip()] = value.strip()
    base.update({k: v for k, v in props.items() if v is not None})
    return full_id(name), tuple(sorted((k, str(v).lower()) for k, v in base.items()))


def props(state):
    return dict(state[1])


def bid(state):
    return state[0][state[0].index(':') + 1:]


def with_props(state, **changes):
    merged = props(state)
    merged.update({k: str(v).lower() for k, v in changes.items()})
    return state[0], tuple(sorted(merged.items()))


# ---------------------------------------------------------------- block traits
def is_air(state):
    return state is None or state[0] in ('minecraft:air', 'minecraft:cave_air', 'minecraft:structure_void')


def is_stairs(state):
    return state is not None and state[0].endswith('_stairs')


def is_fence(state):
    return state is not None and state[0].endswith('_fence')


def is_gate(state):
    return state is not None and state[0].endswith('_fence_gate')


def is_pane(state):
    return state is not None and (state[0].endswith('glass_pane') or state[0] == 'minecraft:iron_bars')


def is_wall(state):
    return state is not None and state[0].endswith('_wall') and 'minecraft:' in state[0]


CONNECTION_EXCEPTIONS = ('_leaves', 'pumpkin', 'melon', 'jack_o_lantern', 'barrier', 'shulker_box')
FULL_SUFFIXES = ('_planks', '_log', '_wood', '_bricks', '_terracotta', '_concrete', '_wool', '_ore', 'stone_bricks',
                 '_glass', 'glass', '_table', 'bookshelf', 'furnace', 'smoker', '_block', 'loom', 'cobblestone')
FULL_IDS = {
    'stone', 'calcite', 'tuff', 'andesite', 'polished_andesite', 'diorite', 'polished_diorite', 'granite',
    'polished_granite', 'deepslate', 'cobbled_deepslate', 'bricks', 'barrel', 'dirt', 'grass_block', 'coarse_dirt',
    'rooted_dirt', 'podzol', 'gravel', 'sand', 'smooth_stone', 'smooth_sandstone', 'sandstone', 'cut_sandstone',
    'chiseled_sandstone', 'packed_mud', 'mud', 'mushroom_stem', 'note_block', 'jukebox', 'dried_kelp_block',
    'target', 'lodestone', 'chiseled_stone_bricks', 'smooth_quartz', 'quartz_bricks', 'clay', 'muddy_mangrove_roots',
    'dirt_path', 'farmland', 'beehive', 'bee_nest', 'stripped_oak_wood', 'chiseled_bookshelf', 'crafting_table',
    'cartography_table', 'fletching_table', 'smithing_table', 'blast_furnace', 'dispenser', 'dropper', 'observer',
    'tnt', 'sponge', 'ice', 'packed_ice', 'snow_block', 'obsidian', 'glowstone', 'sea_lantern', 'redstone_lamp',
    'honeycomb_block', 'prismarine', 'end_stone', 'netherrack', 'basalt', 'polished_basalt', 'blackstone',
    'polished_blackstone', 'mud_bricks', 'tuff_bricks', 'polished_tuff', 'chiseled_tuff', 'archives',
}


def full_cube(state):
    if is_air(state):
        return False
    name = bid(state)
    if any(e in name for e in CONNECTION_EXCEPTIONS):
        return False
    if name.endswith('_slab'):
        return props(state).get('type') == 'double'
    if name.endswith(('_stairs', '_fence', '_fence_gate', '_wall', '_pane', '_door', '_trapdoor', '_carpet',
                      '_pressure_plate', '_button', '_sign', '_banner', '_bed', 'lantern', 'torch', '_rod')):
        return False
    if state[0].startswith(NS + ':'):
        return name == 'archives'
    return name in FULL_IDS or name.endswith(FULL_SUFFIXES)


def sturdy(state, face):
    """Whether ``state`` presents a full face toward ``face`` (a horizontal direction from the block)."""
    if is_stairs(state):
        return props(state).get('facing') == face
    return full_cube(state)


POST_OVERRIDES = ('torch', 'lantern', 'sign', 'banner', 'redstone_wall_torch', 'end_rod', 'campfire',
                  'flower_pot', 'potted_', 'skull', 'head', 'candle', 'chain', 'iron_chain')


def gate_connects(gate, direction):
    return AXIS[props(gate).get('facing', 'north')] == AXIS[CLOCKWISE[direction]]


# ------------------------------------------------------------------- the canvas
class Build:
    """Sparse voxel canvas for one template."""

    def __init__(self, name, size, kind='building', background='air'):
        self.name = name
        self.w, self.h, self.d = size
        self.kind = kind
        # 'structure_void' keeps the world's own blocks wherever nothing is drawn.
        self.background = background
        self.grid = {}
        self.nbt = {}
        self.entities = []
        self.rooms = []
        self.locked = set()
        self.source = None

    # ---- access
    def inside(self, x, y, z):
        return 0 <= x < self.w and 0 <= y < self.h and 0 <= z < self.d

    def get(self, x, y, z):
        return self.grid.get((x, y, z), AIR)

    def set(self, x, y, z, spec, nbt=None, lock=False, clip=False, **kw):
        if not self.inside(x, y, z):
            if clip:
                return
            raise AssertionError(f'{self.name}: block outside template at {(x, y, z)} size {(self.w, self.h, self.d)}')
        state = spec if isinstance(spec, tuple) and not kw else block(spec, **kw)
        pos = (x, y, z)
        if state[0] == 'minecraft:air' and self.background == 'air':
            self.grid.pop(pos, None)
        else:
            self.grid[pos] = state
        self.nbt.pop(pos, None)
        self.locked.discard(pos)
        if nbt is not None:
            self.nbt[pos] = nbt
        if lock:
            self.locked.add(pos)
        return state

    def __call__(self, x, y, z, spec, **kw):
        return self.set(x, y, z, spec, **kw)

    def fill(self, x0, y0, z0, x1, y1, z1, spec, only_air=False, clip=False, **kw):
        state = block(spec, **kw) if not isinstance(spec, tuple) or kw else spec
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    if only_air and not is_air(self.get(x, y, z)):
                        continue
                    self.set(x, y, z, state, clip=clip)

    def clear(self, x0, y0, z0, x1, y1, z1):
        self.fill(x0, y0, z0, x1, y1, z1, 'air', clip=True)

    def natural_ground(self, y=0):
        """Leave the world's own ground wherever nothing was drawn on layer ``y``."""
        for x in range(self.w):
            for z in range(self.d):
                if (x, y, z) not in self.grid:
                    self.grid[(x, y, z)] = ('minecraft:structure_void', ())

    def replace(self, x0, y0, z0, x1, y1, z1, old, new):
        old_id = full_id(old)
        for (x, y, z), state in list(self.grid.items()):
            if min(x0, x1) <= x <= max(x0, x1) and min(y0, y1) <= y <= max(y0, y1) and min(z0, z1) <= z <= max(z0, z1):
                if state[0] == old_id:
                    self.set(x, y, z, new)

    # ---- multi-block helpers with the state pairs Minecraft requires
    def door(self, x, y, z, facing='north', wood='oak', hinge='left', open_=False):
        for dy, half in ((0, 'lower'), (1, 'upper')):
            self.set(x, y + dy, z, f'{wood}_door', facing=facing, half=half, hinge=hinge, open=open_, powered=False)

    def bed(self, x, y, z, facing='north', color='red'):
        """Foot at (x, y, z); the head lies one block toward ``facing``."""
        dx, dz = DIRS[facing]
        self.set(x, y, z, f'{color}_bed', nbt={'id': 'minecraft:bed'}, facing=facing, part='foot', occupied=False)
        self.set(x + dx, y, z + dz, f'{color}_bed', nbt={'id': 'minecraft:bed'}, facing=facing, part='head', occupied=False)

    def chest(self, x, y, z, facing='south', loot=None):
        nbt = {'id': 'minecraft:chest'}
        if loot:
            nbt['LootTable'] = loot
        self.set(x, y, z, 'chest', nbt=nbt, facing=facing, type='single', waterlogged=False)

    def barrel(self, x, y, z, facing='up', loot=None):
        nbt = {'id': 'minecraft:barrel', 'LootTable': loot} if loot else None
        self.set(x, y, z, 'barrel', nbt=nbt, facing=facing, open=False)

    def custom(self, x, y, z, name, facing='north'):
        entity = name in {'house_plaque', 'notice_board', 'command_desk', 'apothecary_cot'}
        self.set(x, y, z, f'{NS}:{name}', nbt={'id': f'{NS}:{name}'} if entity else None, facing=facing)

    def jigsaw(self, x, y, z, orientation, name, target='unused', pool='minecraft:empty', final='minecraft:air',
               joint='aligned', selection=0, placement=0):
        name = name if ':' in name else f'{NS}:{name}'
        target = target if ':' in target else f'{NS}:{target}'
        pool = pool if ':' in pool else f'{NS}:village/{pool}'
        self.set(x, y, z, 'jigsaw', orientation=orientation, nbt={
            'id': 'minecraft:jigsaw', 'name': name, 'target': target, 'pool': pool, 'final_state': final,
            'joint': joint, 'selection_priority': selection, 'placement_priority': placement})

    def entrance(self, x, y=1, z=0):
        """The drop-in contract: north-facing ``building_entrance`` that becomes air."""
        self.jigsaw(x, y, z, 'north_up', 'building_entrance')

    def resident(self, x, y, z, job='none', child=False, tags=()):
        """A villager; ``tags`` become entity tags (a homestead's role, such as ``villagefriends.dweller.pariah``)."""
        profession = 'minecraft:none' if job == 'none' else (job if ':' in job else f'{NS}:{job}')
        nbt = {'id': 'minecraft:villager', 'PersistenceRequired': True, 'Age': -24000 if child else 0,
               'VillagerData': {'type': 'minecraft:plains', 'profession': profession, 'level': 1},
               'Xp': 1 if job != 'none' else 0}
        if tags:
            nbt['Tags'] = list(tags)
        self.entities.append({'pos': [x + .5, float(y), z + .5], 'blockPos': [x, y, z], 'nbt': nbt})

    def animal(self, x, y, z, kind, baby=False, **extra):
        """A persistent animal; ``extra`` adds entity NBT such as a sheep's ``Color``."""
        nbt = {'id': full_id(kind), 'PersistenceRequired': True, **extra}
        if baby:
            nbt['Age'] = -24000
        self.entities.append({'pos': [x + .5, float(y), z + .5], 'blockPos': [x, y, z], 'nbt': nbt})

    def sign(self, x, y, z, lines, facing='north', wood='spruce', wall=True, color='black'):
        """A sign reading ``lines`` (up to four) on its front. ``facing`` is the side the text faces."""
        text = (list(lines) + [''] * 4)[:4]
        sides = {'messages': text, 'color': color, 'has_glowing_text': False}
        nbt = {'id': 'minecraft:sign', 'front_text': sides,
               'back_text': {'messages': [''] * 4, 'color': 'black', 'has_glowing_text': False}, 'is_waxed': True}
        if wall:
            self.set(x, y, z, f'{wood}_wall_sign', nbt=nbt, facing=facing, waterlogged=False)
        else:
            rotation = {'south': 0, 'west': 4, 'north': 8, 'east': 12}[facing]
            self.set(x, y, z, f'{wood}_sign', nbt=nbt, rotation=rotation, waterlogged=False)

    def room(self, name, probe):
        """Record an enclosed room: ``probe`` is a standing-height air cell inside it."""
        self.rooms.append({'name': name, 'probe_cell': list(probe)})

    def mirrored(self, name):
        """Copy mirrored east-west (X), with every directional state flipped to match."""
        swap = {'east': 'west', 'west': 'east', 'left': 'right', 'right': 'left', 'inner_left': 'inner_right',
                'inner_right': 'inner_left', 'outer_left': 'outer_right', 'outer_right': 'outer_left',
                'east_up': 'west_up', 'west_up': 'east_up'}
        out = Build(name, (self.w, self.h, self.d), self.kind, self.background)
        for (x, y, z), state in self.grid.items():
            p = props(state)
            q = {}
            for k, v in p.items():
                if k in ('east', 'west'):
                    q[swap[k]] = v
                elif k in ('facing', 'hinge', 'shape', 'orientation'):
                    q[k] = swap.get(v, v)
                elif k == 'rotation':
                    q[k] = str((16 - int(v)) % 16)
                else:
                    q[k] = v
            mx = self.w - 1 - x
            out.grid[(mx, y, z)] = (state[0], tuple(sorted(q.items())))
            if (x, y, z) in self.nbt:
                out.nbt[(mx, y, z)] = dict(self.nbt[(x, y, z)])
            if (x, y, z) in self.locked:
                out.locked.add((mx, y, z))
        for e in self.entities:
            e2 = json.loads(json.dumps(e))
            e2['pos'][0] = self.w - e['pos'][0]
            e2['blockPos'][0] = self.w - 1 - e['blockPos'][0]
            out.entities.append(e2)
        for r in self.rooms:
            r2 = dict(r)
            if 'probe_cell' in r2:
                r2['probe_cell'] = [self.w - 1 - r['probe_cell'][0]] + list(r['probe_cell'][1:])
            out.rooms.append(r2)
        return out

    # ------------------------------------------------------------ finishing
    def _connect(self):
        for pos, state in list(self.grid.items()):
            if pos in self.locked:
                continue
            x, y, z = pos
            if is_fence(state) or is_pane(state) or is_wall(state):
                sides = {}
                for direction, (dx, dz) in DIRS.items():
                    other = self.grid.get((x + dx, y, z + dz))
                    if other is None:
                        sides[direction] = False
                    elif is_fence(state):
                        wooden = 'nether_brick' not in state[0]
                        sides[direction] = (is_fence(other) and ('nether_brick' not in other[0]) == wooden) \
                            or (is_gate(other) and gate_connects(other, direction)) \
                            or sturdy(other, OPPOSITE[direction])
                    elif is_pane(state):
                        sides[direction] = is_pane(other) or is_wall(other) or sturdy(other, OPPOSITE[direction])
                    else:
                        sides[direction] = is_wall(other) or is_pane(other) or (
                            is_gate(other) and gate_connects(other, direction)) or sturdy(other, OPPOSITE[direction])
                if is_wall(state):
                    above = self.grid.get((x, y + 1, z))
                    tall = above is not None and full_cube(above)
                    values = {k: ('tall' if tall else 'low') if v else 'none' for k, v in sides.items()}
                    n, s, e, w = (sides[k] for k in ('north', 'south', 'east', 'west'))
                    corner = (not (n or s or e or w)) or n != s or e != w
                    straight_tall = tall and ((n and s) or (e and w))
                    post_override = above is not None and any(t in bid(above) for t in POST_OVERRIDES)
                    up = corner or (not straight_tall and (post_override or tall))
                    self.grid[pos] = with_props(state, up=up, waterlogged=False, **values)
                else:
                    self.grid[pos] = with_props(state, waterlogged=False, **sides)
        for pos, state in list(self.grid.items()):
            if is_stairs(state) and pos not in self.locked and 'shape' not in props(state):
                self.grid[pos] = with_props(state, shape=self._stair_shape(pos, state))
            elif is_stairs(state) and 'waterlogged' not in props(state):
                self.grid[pos] = with_props(state, waterlogged=False)

    def _stair_shape(self, pos, state):
        x, y, z = pos
        p = props(state)
        facing, half = p.get('facing', 'north'), p.get('half', 'bottom')

        def stairs_at(direction):
            dx, dz = DIRS[direction]
            other = self.grid.get((x + dx, y, z + dz))
            return other if is_stairs(other) and props(other).get('half', 'bottom') == half else None

        def can_take(direction):
            dx, dz = DIRS[direction]
            other = self.grid.get((x + dx, y, z + dz))
            return not is_stairs(other) or props(other).get('facing', 'north') != facing \
                or props(other).get('half', 'bottom') != half

        front = stairs_at(facing)
        if front:
            f1 = props(front).get('facing', 'north')
            if AXIS[f1] != AXIS[facing] and can_take(OPPOSITE[f1]):
                return 'outer_left' if f1 == COUNTER[facing] else 'outer_right'
        back = stairs_at(OPPOSITE[facing])
        if back:
            f2 = props(back).get('facing', 'north')
            if AXIS[f2] != AXIS[facing] and can_take(f2):
                return 'inner_left' if f2 == COUNTER[facing] else 'inner_right'
        return 'straight'

    def _open_for_rooms(self, state):
        """Union of the compiler's and Minecraft's notion of a walkable/open cell."""
        if is_air(state):
            return True
        name = bid(state)
        if state[0].startswith(NS + ':'):
            return name != 'house_plaque'
        return name in ('lantern', 'wall_torch', 'torch', 'ladder', 'flower_pot', 'short_grass', 'chain', 'iron_chain') \
            or name.startswith('potted_') or name.endswith(('_pressure_plate', '_button', '_sign', '_banner')) \
            or name in ('poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium')

    def _finish_rooms(self):
        regions = []
        for room in self.rooms:
            if 'probe_cell' not in room:
                continue
            start = tuple(room.pop('probe_cell'))
            assert self._open_for_rooms(self.get(*start)), f'{self.name}/{room["name"]}: probe {start} is not open'
            seen, queue = {start}, deque([start])
            while queue:
                x, y, z = queue.popleft()
                assert 0 < x < self.w - 1 and 0 < y < self.h - 1 and 0 < z < self.d - 1, \
                    f'{self.name}/{room["name"]}: room leaks at {(x, y, z)}'
                assert len(seen) < 4000, f'{self.name}/{room["name"]}: room is not enclosed'
                for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    p = (x + dx, y + dy, z + dz)
                    if p not in seen and self._open_for_rooms(self.get(*p)):
                        seen.add(p)
                        queue.append(p)
            assert len(seen) <= 250, f'{self.name}/{room["name"]}: bedroom leaks into a larger space ({len(seen)} cells)'
            for other in regions:
                assert not (seen & other[1]), f'{self.name}: bedrooms {other[0]} and {room["name"]} connect'
            regions.append((room['name'], seen))
            lo = [min(p[i] for p in seen) for i in range(3)]
            hi = [max(p[i] for p in seen) for i in range(3)]
            # The compiler probes one block above ``probe``; Minecraft does the same.
            probe = [start[0], start[1] - 1, start[2]]
            room.update({'min': lo, 'max': hi, 'probe': probe})
            # Keep min at the probe's level so ``min`` doubles as the probe, as in earlier blueprints.
            room['min'][1] = min(room['min'][1], probe[1])

    def _passable(self, state):
        """Minecraft's structure test: air, lanterns, ladders, torches or no collision (doors never)."""
        if is_air(state):
            return True
        name = bid(state)
        if name.endswith('_door'):
            return False
        return name in ('lantern', 'ladder', 'torch', 'wall_torch', 'short_grass', 'tall_grass', 'fern', 'vine',
                        'sugar_cane', 'redstone_wire', 'rail', 'chain', 'iron_chain') \
            or name.endswith(('_pressure_plate', '_button', '_sign', '_banner', '_sapling', '_tulip')) \
            or name in ('poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium',
                        'lily_of_the_valley', 'wheat', 'carrots', 'potatoes', 'beetroots')

    def _check_doors(self):
        for (x, y, z), state in self.grid.items():
            if not state[0].endswith('_door') or props(state).get('half') != 'lower':
                continue
            dx, dz = DIRS[props(state).get('facing', 'north')]
            for sx, sz in ((x + dx, z + dz), (x - dx, z - dz)):
                for h in (0, 1):
                    cell = (sx, y + h, sz)
                    if self.inside(*cell):
                        # Lanterns and chains have collision boxes: fine in a room, not in a doorway.
                        assert self._passable(self.get(*cell)) and bid(self.get(*cell)) not in ('lantern', 'chain', 'iron_chain'), \
                            f'{self.name}: door at {(x, y, z)} needs two clear blocks on both sides; {cell} is {self.get(*cell)[0]}'

    def finish(self):
        self._connect()
        self._finish_rooms()
        self._check_doors()
        return self

    # ------------------------------------------------------------- export
    def blueprint(self):
        symbols = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,-/:;<=>?@[]^_{|}~')
        symbols += [chr(c) for c in range(0xC0, 0x250) if chr(c) not in '×÷']
        symbols += [chr(c) for c in range(0x391, 0x3CA) if chr(c).isalpha()]
        symbols += [chr(c) for c in range(0x410, 0x450)]
        void = ('minecraft:structure_void', ())
        cells = {(x, y, z): self.grid.get((x, y, z), AIR if self.background == 'air' else void)
                 for x in range(self.w) for y in range(self.h) for z in range(self.d)}
        counts = Counter(s for s in cells.values() if s != AIR)
        order = sorted(counts, key=lambda s: (-counts[s], s))
        assert len(order) <= len(symbols), f'{self.name}: too many block states'
        key = {state: symbols[i] for i, state in enumerate(order)}
        palette = {'.': {'id': 'minecraft:air'}}
        for state in order:
            entry = {'id': state[0]}
            if state[1]:
                entry['properties'] = dict(state[1])
            palette[key[state]] = entry
        layers = []
        for y in range(self.h):
            rows = [''.join(key.get(cells[(x, y, z)], '.') for x in range(self.w)) for z in range(self.d)]
            layers.append({'y': y, 'rows': rows})
        data = {'format': 1, 'size': [self.w, self.h, self.d], 'palette': palette, 'layers': layers,
                'block_entities': [{'pos': list(p), 'nbt': n} for p, n in sorted(self.nbt.items())],
                'entities': self.entities, 'rooms': self.rooms}
        if self.source:
            data['design'] = {'source': self.source, 'checksum': checksum(data)}
        return data


def checksum(data):
    body = {k: v for k, v in data.items() if k != 'design'}
    return hashlib.sha1(json.dumps(body, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]


def dump(data):
    """Compact, diff-friendly JSON: one blueprint row per line."""
    text = json.dumps(data, indent=1, ensure_ascii=False)
    # Collapse small leaf dicts/lists onto one line for readability.
    text = re.sub(r'\[\s+([-\d.,\s]+?)\s+\]', lambda m: '[' + ', '.join(v.strip() for v in m.group(1).split(',')) + ']', text)
    return text + '\n'
