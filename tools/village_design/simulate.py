"""Approximate Minecraft's jigsaw assembly in 2D to tune the village layout.

    python tools/village_design/simulate.py --seeds 200          # statistics
    python tools/village_design/simulate.py --map 3 --out build   # top-down map PNGs (needs Pillow)

It follows JigsawPlacement's breadth-first order, selection priorities, weighted
shuffles, empty-element early exit, fallback pools, rotations, the max-distance
box and non-overlapping bounding boxes, on flat ground. Minecraft remains the
authority (``gradlew runClientGameTest -PstructuresOnly``).
"""
import argparse
import json
import random
import sys
from collections import Counter, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NS = 'villagefriends'
TURN = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}
OPP = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
STEP = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}


def load():
    layout = json.loads((ROOT / 'village_layout.json').read_text())
    templates = {}
    for path in sorted((ROOT / 'village_blueprints').glob('*.json')):
        data = json.loads(path.read_text(encoding='utf-8'))
        w, h, d = data['size']
        jigsaws = []
        for e in data['block_entities']:
            n = e['nbt']
            if n.get('id') != 'minecraft:jigsaw':
                continue
            x, y, z = e['pos']
            row = data['layers'][y]['rows'][z][x]
            orient = data['palette'][row]['properties']['orientation'].split('_')[0]
            if orient in ('up', 'down'):
                continue
            jigsaws.append({'pos': (x, z), 'facing': orient, 'name': n['name'], 'target': n['target'],
                            'pool': n['pool'], 'sel': n.get('selection_priority', 0)})
        templates[path.stem] = {'size': (w, d), 'jigsaws': jigsaws,
                                'residents': len(data.get('entities', []))}
    pools = {}
    for name, spec in layout['pools'].items():
        if isinstance(spec, list):
            spec = {'elements': spec, 'fallback': 'minecraft:empty'}
        pools[f'{NS}:village/{name}'] = {
            'elements': [(e['template'], e['weight']) for e in spec['elements']],
            'fallback': spec.get('fallback', 'minecraft:empty') if spec.get('fallback', 'minecraft:empty') == 'minecraft:empty'
            else f'{NS}:village/{spec["fallback"]}'}
    return layout, templates, pools


def rotate(x, z, r):
    for _ in range(r):
        x, z = -z, x
    return x, z


def turn(f, r):
    for _ in range(r):
        f = TURN[f]
    return f


def placed_box(t, r, origin):
    w, d = t['size']
    xs, zs = [], []
    for cx, cz in ((0, 0), (w - 1, 0), (0, d - 1), (w - 1, d - 1)):
        x, z = rotate(cx, cz, r)
        xs.append(x + origin[0])
        zs.append(z + origin[1])
    return (min(xs), min(zs), max(xs), max(zs))


def overlaps(a, b):
    return not (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1])


def shuffled(pool, rng):
    items = []
    for name, weight in pool['elements']:
        items += [name] * weight
    rng.shuffle(items)
    return items


def assemble(layout, templates, pools, seed):
    rng = random.Random(seed)
    depth_max = layout['depth']
    dist = layout['max_distance']
    start = layout['pools']['town_centers']
    start_names = [e['template'] for e in start]
    name = rng.choice(start_names)
    t = templates[name]
    r = rng.randrange(4)
    sj = next(j for j in json.loads((ROOT / 'village_blueprints' / f'{name}.json').read_text())['block_entities']
              if j['nbt'].get('name') == layout['start_jigsaw'])
    sx, sz = rotate(sj['pos'][0], sj['pos'][2], r)
    origin = (-sx, -sz)
    bounds = (-dist, -dist, dist, dist)
    pieces = [{'name': name, 'rot': r, 'origin': origin, 'box': placed_box(t, r, origin), 'depth': 0}]
    queue = deque([pieces[0]])
    while queue:
        piece = queue.popleft()
        t = templates[piece['name']]
        js = list(t['jigsaws'])
        rng.shuffle(js)
        js.sort(key=lambda j: -j['sel'])
        for j in js:
            if j['pool'] == 'minecraft:empty':
                continue
            jx, jz = rotate(*j['pos'], piece['rot'])
            jx, jz = jx + piece['origin'][0], jz + piece['origin'][1]
            facing = turn(j['facing'], piece['rot'])
            tx, tz = jx + STEP[facing][0], jz + STEP[facing][1]
            pool = pools[j['pool']]
            cands = []
            if piece['depth'] != depth_max:
                cands += shuffled(pool, rng)
            if pool['fallback'] != 'minecraft:empty':
                cands += shuffled(pools[pool['fallback']], rng)
            done = False
            for cname in cands:
                if cname == 'empty':
                    break
                ct = templates[cname]
                rots = [0, 1, 2, 3]
                rng.shuffle(rots)
                for cr in rots:
                    cjs = list(ct['jigsaws'])
                    rng.shuffle(cjs)
                    for cj in cjs:
                        if cj['name'] != j['target'] or turn(cj['facing'], cr) != OPP[facing]:
                            continue
                        cx, cz = rotate(*cj['pos'], cr)
                        corigin = (tx - cx, tz - cz)
                        box = placed_box(ct, cr, corigin)
                        if box[0] < bounds[0] or box[1] < bounds[1] or box[2] > bounds[2] or box[3] > bounds[3]:
                            continue
                        if any(overlaps(box, p['box']) for p in pieces):
                            continue
                        child = {'name': cname, 'rot': cr, 'origin': corigin, 'box': box, 'depth': piece['depth'] + 1,
                                 'pool': j['pool']}
                        pieces.append(child)
                        if child['depth'] <= depth_max:
                            queue.append(child)
                        done = True
                        break
                    if done:
                        break
                if done:
                    break
    return pieces


def draw(pieces, templates, path, layout):
    from PIL import Image, ImageDraw
    dist = layout['max_distance']
    s = 3
    img = Image.new('RGB', ((2 * dist + 1) * s, (2 * dist + 1) * s), (110, 160, 80))
    g = ImageDraw.Draw(img)
    for p in pieces:
        x0, z0, x1, z1 = p['box']
        n = p['name']
        col = (150, 150, 150) if n.startswith(('street', 'avenue', 'end_')) or 'plaza' in n else \
            (200, 90, 60) if p.get('pool', '').endswith(('tavern', 'garrison', 'workshop', 'chapel', 'apothecary', 'library')) else \
            (220, 200, 120) if 'farm' in n or 'pen' in n else (90, 130, 200) if 'decor' in n else (170, 110, 60)
        g.rectangle([(x0 + dist) * s, (z0 + dist) * s, (x1 + dist + 1) * s - 1, (z1 + dist + 1) * s - 1],
                    fill=col, outline=(40, 40, 40))
    img.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', type=int, default=100)
    parser.add_argument('--map', type=int, default=0)
    parser.add_argument('--out', default='build')
    args = parser.parse_args()
    layout, templates, pools = load()
    required = [f'{NS}:village/{p}' for p in layout['required_pools'] if p != 'town_centers']
    counts, residents, missing, kinds = [], [], Counter(), Counter()
    for seed in range(args.seeds):
        pieces = assemble(layout, templates, pools, seed)
        counts.append(len(pieces))
        residents.append(sum(templates[p['name']]['residents'] for p in pieces))
        present = {p.get('pool') for p in pieces}
        for r in required:
            if r not in present:
                missing[r] += 1
        for p in pieces:
            kinds[p['name']] += 1
        if seed < args.map:
            out = Path(args.out)
            out.mkdir(parents=True, exist_ok=True)
            draw(pieces, templates, out / f'village_map_{seed}.png', layout)
    counts.sort()
    print(f'pieces: min {counts[0]}  median {counts[len(counts) // 2]}  max {counts[-1]}')
    residents.sort()
    print(f'residents: min {residents[0]}  median {residents[len(residents) // 2]}  max {residents[-1]}')
    print('required pools missing:', dict(missing) or 'never')
    print('average per village:', ', '.join(f'{k} {v / args.seeds:.1f}' for k, v in kinds.most_common()))


if __name__ == '__main__':
    main()
