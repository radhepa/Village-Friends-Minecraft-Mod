"""Package the editable gendered name pools; optionally refresh the general pool from a numbered markdown list.

tools/name_pools.json (version 2) is the source of truth. Every pool lists male, female and unisex
first names separately; non-binary residents draw unisex names. A pool may carry its own surnames.
The 'indian' pool is limited to brown and darker complexions (2-5), and none of its names or
surnames may appear anywhere a lighter complexion could draw them. Document prose is never executed.
"""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'tools/name_pools.json'
TARGET = ROOT/'src/main/resources/data/villagefriends/villagefriends/names.json'
GENDERS = ('male', 'female', 'unisex')
# Names in the Boys/Girls lists that are worn by everyone; they go to the unisex list.
UNISEX = set('Avery Bryn Drew Emery Ellis Robin Rowan Raven Morgan Peyton Quinn Wren Gwyn Sage Loren Sawyer Parker Kai Sheridan'.split())
NOT_NAMES = {'Xenon'}


def unique(values):
    return list(dict.fromkeys(v.strip() for v in values if v.strip()))


def refresh_general(data, markdown):
    sections = {}
    for section in re.split(r'^## ', markdown.read_text(encoding='utf-8-sig'), flags=re.M)[1:]:
        sections[section.splitlines()[0].split(' ')[0]] = unique(re.findall(r'^\s*\d+\.\s+(.+?)\s*$', section, flags=re.M))
    assert all(k in sections for k in ('Boys', 'Girls')), 'markdown needs ## Boys and ## Girls sections'
    boys, girls = sections['Boys'], sections['Girls']
    general = next(p for p in data['pools'] if p['id'] == 'general')
    shared = {n for n in boys if n in girls} | UNISEX
    general['male'] = [n for n in boys if n not in shared and n not in NOT_NAMES]
    general['female'] = [n for n in girls if n not in shared]
    general['unisex'] = unique([n for n in boys + girls if n in shared] + general.get('unisex', []))


def check(data):
    assert data['version'] == 2, 'name_pools.json must be version 2'
    indian = next(p for p in data['pools'] if p['id'] == 'indian')
    assert min(indian['complexions']) >= 2, 'Indian names are for brown and darker complexions only'
    restricted = {n.casefold() for k in GENDERS + ('surnames',) for n in indian.get(k, [])}
    for pool in data['pools']:
        for i, a in enumerate(GENDERS):
            for b in GENDERS[i+1:]:
                both = set(pool[a]) & set(pool[b])
                assert not both, f"{pool['id']}: {sorted(both)} listed as both {a} and {b}"
        if min(pool['complexions']) < 2 and pool is not indian:
            leak = [n for k in GENDERS + ('surnames',) for n in pool.get(k, []) if n.casefold() in restricted]
            assert not leak, f"{pool['id']} leaks Indian names to light complexions: {leak}"
    leak = [s for s in data['surnames'] if s.casefold() in restricted]
    assert not leak, f'general surnames leak Indian surnames: {leak}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='Refresh the general pool from a markdown list with ## Boys / ## Girls sections.')
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text(encoding='utf-8'))
    if args.source:
        refresh_general(data, args.source)
        for pool in data['pools']:
            for k in GENDERS: pool[k] = unique(pool[k])
    check(data)
    if args.source: SOURCE.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Packaged name pools:', {p['id']: {k: len(p[k]) for k in GENDERS} for p in data['pools']},
          'surnames:', len(data['surnames'])+len(data['restrictedSurnames']))


if __name__ == '__main__': main()
