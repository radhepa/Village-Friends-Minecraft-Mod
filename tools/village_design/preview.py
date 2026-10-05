"""Isometric previews of blueprints (development aid; needs Pillow).

    python tools/village_design/preview.py tavern cottage_oak --out build/previews

Colours are averaged from the vanilla block textures (``texture_colors.json``),
so silhouettes, rooflines and palettes read correctly. Final checks still
belong in Minecraft (``gradlew runClientGameTest -PvillageGallery``).
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLUEPRINTS = HERE.parent / 'village_blueprints'
COLORS = json.loads((HERE / 'texture_colors.json').read_text())
WOODS = ('oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak', 'mangrove', 'cherry', 'pale_oak', 'bamboo',
         'crimson', 'warped')
TINT = (145, 189, 89)
LEAF_TINT = (119, 171, 47)
SUFFIXES = ('_stairs', '_slab', '_wall', '_fence_gate', '_fence', '_pressure_plate', '_button', '_carpet',
            '_trapdoor', '_door', '_pane', '_wall_banner', '_banner', '_bed', '_wall_sign', '_sign')


def _lookup(*names):
    for name in names:
        if name in COLORS:
            return COLORS[name]
    return None


def color(name, face, props):
    special = {'water': (63, 118, 228), 'lava': (207, 92, 20), 'air': None, 'jigsaw': None,
               'structure_void': None, 'lantern': (200, 150, 70), 'campfire': (210, 120, 40),
               'bell': (230, 190, 60), 'chain': (60, 60, 70), 'composter': (110, 80, 40)}
    if name in special:
        return special[name]
    base = name
    for suffix in SUFFIXES:
        if base.endswith(suffix):
            base = base[:-len(suffix)]
            break
    if name.endswith(('_bed', '_carpet', '_wool', '_banner', '_wall_banner')):
        base = name.split('_bed')[0].split('_carpet')[0].split('_wall_banner')[0].split('_banner')[0]
        found = _lookup(base + '_wool')
        if found:
            return found[:3]
    candidates = []
    if face == 'top':
        candidates += [name + '_top', base + '_top']
    candidates += [name, name + '_side', base, base + 's', base + '_planks', base + '_side', base + '_bricks',
                   base.replace('_tile', '_tiles'), base.replace('brick', 'bricks'), base + '_block']
    if base in WOODS:
        candidates.insert(0, base + '_planks')
    if name.startswith('potted_'):
        candidates = [name[7:], 'flower_pot']
    if name.startswith('stripped_') and (name.endswith('_log') or name.endswith('_wood')):
        candidates = [name if face != 'top' else name + '_top', name]
    if 'smooth_sandstone' in name:
        candidates = ['sandstone_top']
    if 'smooth_stone' in name:
        candidates = ['smooth_stone']
    found = _lookup(*candidates)
    if found is None and name.endswith(('_door',)):
        found = _lookup(name + '_bottom')
    if found is None and 'glass' in name:
        found = (170, 200, 215)
    if found is None:
        return (150, 110, 70) if props.get('_mod') else (200, 0, 200)
    rgb = tuple(found[:3])
    if name in ('grass_block',) and face == 'top' or name in ('short_grass', 'tall_grass', 'fern', 'vine', 'lily_pad'):
        rgb = tuple(int(c * t / 255) for c, t in zip(rgb, TINT))
    elif name.endswith('_leaves') and not any(k in name for k in ('cherry', 'azalea', 'pale')):
        rgb = tuple(int(c * t / 255) for c, t in zip(rgb, LEAF_TINT))
    if name == 'grass_block' and face != 'top':
        rgb = tuple(COLORS['dirt'][:3])
    return rgb


def boxes(name, p, below_name=None):
    """Approximate collision/visual boxes in 1/16 block units."""
    half = p.get('half')
    if name.endswith('_slab'):
        t = p.get('type', 'bottom')
        return [(0, 0, 0, 16, 16, 16)] if t == 'double' else [(0, 0 if t == 'bottom' else 8, 0, 16, 8 if t == 'bottom' else 16, 16)]
    if name.endswith('_stairs'):
        f = p.get('facing', 'north')
        bottom = (0, 0, 0, 16, 8, 16) if half != 'top' else (0, 8, 0, 16, 16, 16)
        y0, y1 = (8, 16) if half != 'top' else (0, 8)
        back = {'north': (0, y0, 0, 16, y1, 8), 'south': (0, y0, 8, 16, y1, 16),
                'west': (0, y0, 0, 8, y1, 16), 'east': (8, y0, 0, 16, y1, 16)}[f]
        return [bottom, back]
    if name.endswith('_fence') or name.endswith('_wall') or name.endswith('_pane') or name == 'iron_bars':
        wall = name.endswith('_wall')
        r = 4 if wall else (2 if name.endswith('_fence') else 1)
        top = 16 if not wall or p.get('up', 'true') == 'true' else 14
        out = [(8 - r, 0, 8 - r, 8 + r, top, 8 + r)]
        arm = 3 if wall else 1
        ay0, ay1 = (0, 14) if wall else ((6, 15) if name.endswith('_fence') else (0, 16))
        for d, box in (('north', (8 - arm, ay0, 0, 8 + arm, ay1, 8)), ('south', (8 - arm, ay0, 8, 8 + arm, ay1, 16)),
                       ('west', (0, ay0, 8 - arm, 8, ay1, 8 + arm)), ('east', (8, ay0, 8 - arm, 16, ay1, 8 + arm))):
            if p.get(d, 'false') not in ('false', 'none'):
                out.append(box)
        return out
    if name.endswith('_fence_gate'):
        return [(0, 5, 7, 16, 15, 9)] if p.get('facing', 'north') in ('north', 'south') else [(7, 5, 0, 9, 15, 16)]
    if name.endswith('_door'):
        f = p.get('facing', 'north')
        if p.get('open') == 'true':
            f = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}[f]
        return [{'north': (0, 0, 13, 16, 16, 16), 'south': (0, 0, 0, 16, 16, 3),
                 'west': (13, 0, 0, 16, 16, 16), 'east': (0, 0, 0, 3, 16, 16)}[f]]
    if name.endswith('_trapdoor'):
        if p.get('open') == 'true':
            f = p.get('facing', 'north')
            return [{'north': (0, 0, 13, 16, 16, 16), 'south': (0, 0, 0, 16, 16, 3),
                     'west': (13, 0, 0, 16, 16, 16), 'east': (0, 0, 0, 3, 16, 16)}[f]]
        return [(0, 13, 0, 16, 16, 16)] if half == 'top' else [(0, 0, 0, 16, 3, 16)]
    if name.endswith('_carpet') or name.endswith('_pressure_plate') or name == 'moss_carpet':
        return [(0, 0, 0, 16, 1, 16)]
    if name.endswith('_bed'):
        return [(0, 0, 0, 16, 9, 16)]
    if name in ('lantern', 'soul_lantern'):
        return [(5, 1, 5, 11, 10, 11)] if p.get('hanging') == 'true' else [(5, 0, 5, 11, 9, 11)]
    if name in ('torch', 'wall_torch', 'end_rod', 'lightning_rod'):
        return [(7, 0, 7, 9, 11, 9)]
    if name == 'chain':
        return [(7, 0, 7, 9, 16, 9)]
    if name in ('campfire', 'soul_campfire'):
        return [(0, 0, 0, 16, 7, 16)]
    if name == 'flower_pot' or name.startswith('potted_'):
        return [(5, 0, 5, 11, 6, 11), (6, 6, 6, 10, 12, 10)] if name.startswith('potted_') else [(5, 0, 5, 11, 6, 11)]
    if name in ('wheat', 'carrots', 'potatoes', 'beetroots'):
        return [(1, 0, 1, 15, 13, 15)]
    if name in ('short_grass', 'fern', 'poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium',
                'lily_of_the_valley', 'red_tulip', 'orange_tulip', 'white_tulip', 'pink_tulip', 'sweet_berry_bush',
                'pink_petals', 'wildflowers', 'bush', 'firefly_bush', 'leaf_litter', 'short_dry_grass'):
        return [(4, 0, 4, 12, 9, 12)]
    if name in ('tall_grass', 'large_fern', 'lilac', 'rose_bush', 'peony', 'sunflower'):
        return [(3, 0, 3, 13, 16, 13)]
    if name in ('bell',):
        return [(4, 4, 4, 12, 13, 12)]
    if name.endswith('_wall_banner') or name.endswith('_banner'):
        f = p.get('facing', 'north')
        return [{'north': (0, 0, 14, 16, 16, 16), 'south': (0, 0, 0, 16, 16, 2),
                 'west': (14, 0, 0, 16, 16, 16), 'east': (0, 0, 0, 2, 16, 16)}.get(f, (6, 0, 6, 10, 16, 10))]
    if name == 'ladder' or name == 'vine':
        return [(0, 0, 0, 16, 16, 2)]
    if name in ('village_bench', 'campfire_bench', 'command_desk', 'sewing_table', 'sawmill'):
        return [(0, 0, 2, 16, 10, 14)]
    if name in ('anvil', 'grindstone', 'stonecutter', 'lectern', 'brewing_stand', 'cauldron', 'composter'):
        return [(1, 0, 1, 15, 14, 15)]
    if name in ('dirt_path', 'farmland'):
        return [(0, 0, 0, 16, 15, 16)]
    return [(0, 0, 0, 16, 16, 16)]


def render(data, scale=12, view='nw', show_ground=True):
    from PIL import Image, ImageDraw
    w, h, d = data['size']
    palette = data['palette']
    voxels = []
    for layer in data['layers']:
        y = layer['y']
        for z, row in enumerate(layer['rows']):
            for x, sym in enumerate(row):
                entry = palette[sym]
                name = entry['id'].split(':')[1]
                if name in ('air', 'jigsaw', 'structure_void'):
                    continue
                vx, vz = (x, z) if view == 'nw' else (w - 1 - x, z) if view == 'ne' else (x, d - 1 - z) if view == 'sw' else (w - 1 - x, d - 1 - z)
                voxels.append((vx, y, vz, name, entry.get('properties', {}), entry['id']))
    import math
    a = math.cos(math.radians(30)) * scale
    b = math.sin(math.radians(30)) * scale
    c = scale
    W = int((w + d) * a) + 2 * scale
    H = int((w + d) * b + h * c) + 2 * scale
    img = Image.new('RGB', (W, H), (178, 206, 244))
    draw = ImageDraw.Draw(img)
    ox = d * a + scale
    oy = (w + d) * b + h * c + scale

    def proj(x, y, z):
        return (ox + (x - z) * a, oy - (x + z) * b - y * c)

    def flipbox(bx):
        x0, y0, z0, x1, y1, z1 = bx
        if view in ('ne', 'se'):
            x0, x1 = 16 - x1, 16 - x0
        if view in ('sw', 'se'):
            z0, z1 = 16 - z1, 16 - z0
        return x0, y0, z0, x1, y1, z1

    def flipprops(p):
        p = dict(p)
        mapping = {}
        if view in ('ne', 'se'):
            mapping.update({'east': 'west', 'west': 'east'})
        if view in ('sw', 'se'):
            mapping.update({'north': 'south', 'south': 'north'})
        if not mapping:
            return p
        out = {}
        for k, v in p.items():
            out[mapping.get(k, k)] = mapping.get(v, v) if k == 'facing' else v
        return out

    items = []
    for vx, y, vz, name, p, full in voxels:
        p2 = flipprops(p)
        for bx in boxes(name, p2):
            items.append((vx, y, vz, name, p, flipbox(bx), full))
    items.sort(key=lambda t: (-(t[0] + t[2]) - (t[5][0] + t[5][2]) / 32, t[1] + t[5][1] / 16))
    for vx, y, vz, name, p, (x0, y0, z0, x1, y1, z1), full in items:
        X0, X1 = vx + x0 / 16, vx + x1 / 16
        Y0, Y1 = y + y0 / 16, y + y1 / 16
        Z0, Z1 = vz + z0 / 16, vz + z1 / 16
        axis = p.get('axis', 'y')
        top_face, side_face = 'top', 'side'
        cols = {}
        for face in ('top', 'west', 'north'):
            kind = 'top' if face == 'top' else 'side'
            if name.endswith(('_log', '_wood', '_stem')) and axis != 'y':
                if face == 'top':
                    kind = 'side'
                elif (axis == 'x' and face == 'west') or (axis == 'z' and face == 'north'):
                    kind = 'top'
            col = color(name, kind, dict(p, _mod=not full.startswith('minecraft:')))
            if col is None:
                cols = None
                break
            cols[face] = col
        if cols is None:
            continue
        shade = {'top': 1.0, 'west': 0.78, 'north': 0.62}
        faces = {
            'top': [proj(X0, Y1, Z0), proj(X1, Y1, Z0), proj(X1, Y1, Z1), proj(X0, Y1, Z1)],
            'west': [proj(X0, Y0, Z0), proj(X0, Y1, Z0), proj(X0, Y1, Z1), proj(X0, Y0, Z1)],
            'north': [proj(X0, Y0, Z0), proj(X1, Y0, Z0), proj(X1, Y1, Z0), proj(X0, Y1, Z0)],
        }
        for face, poly in faces.items():
            rgb = tuple(min(255, int(v * shade[face])) for v in cols[face])
            edge = tuple(int(v * 0.8) for v in rgb)
            draw.polygon(poly, fill=rgb, outline=edge)
    return img


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('names', nargs='*')
    parser.add_argument('--out', default='build/previews')
    parser.add_argument('--scale', type=int, default=12)
    parser.add_argument('--views', default='nw,se')
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    names = args.names or [p.stem for p in sorted(BLUEPRINTS.glob('*.json'))]
    for name in names:
        data = json.loads((BLUEPRINTS / f'{name}.json').read_text(encoding='utf-8'))
        for view in args.views.split(','):
            render(data, args.scale, view).save(out / f'{name}_{view}.png')
    print(f'Wrote previews for {len(names)} blueprints to {out}')


if __name__ == '__main__':
    main()
