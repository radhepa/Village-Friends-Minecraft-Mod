"""Horse gear: the data table Java reads (stablehand/gear.json), and later the equipment layers, entity
textures, item sprites, recipes and the caparison dye recipe.

Each row is one item. `kind` barding goes in the BODY slot (horse armor), `kind` tack in the SADDLE slot.
Barding: armor `defense`, `toughness`, `knockback` resistance, `enchantability` and the `repair` item tag;
`dyeable` cloth with its `undyed` colour (signed ARGB). Tack: `columns` of pack slots it gives (3 slots
each; the vanilla mount screen fits at most 5), `bond_ride` (how much faster riding grows the bond) and
`calm` (how much steadier the horse is near monsters). `animals` says which of horse, donkey and mule may
wear it.

The lance is vanilla's kinetic spear with its own numbers (Item.Properties.spear order, then the attack
reach): damage needs at least `damage_threshold` blocks per second of closing speed, so it lands only from
a galloping horse (a sprinting player makes about 5.6).

Never hand-edit gear.json; change the rows here and rerun tools/stablehand/stablehand.py.
"""
from kit import TABLES, dump

CLOTH_RED = -6537410  # 0x9C3F3E with full alpha, as a signed int

GEAR = [
    # id, kind, slot, animals, defense, toughness, knockback, enchantability, repair, dyeable, undyed, columns, bond_ride, calm
    ('caparison', 'barding', 'body', ['horse'], 2, 0, 0, 15, 'minecraft:wool', True, CLOTH_RED, 0, 1.0, 0),
    ('leather_barding', 'barding', 'body', ['horse'], 4, 0, 0, 15, 'minecraft:repairs_leather_armor', False, 0, 0, 1.0, 0),
    ('mail_barding', 'barding', 'body', ['horse'], 6, 0, 0, 12, 'minecraft:repairs_chain_armor', False, 0, 0, 1.0, 0),
    ('plate_barding', 'barding', 'body', ['horse'], 10, 2, 0.1, 9, 'minecraft:repairs_iron_armor', False, 0, 0, 1.0, 0),
    ('saddlebags', 'tack', 'saddle', ['horse'], 0, 0, 0, 0, '', False, 0, 2, 1.0, 0),
    ('bridle', 'tack', 'saddle', ['horse', 'donkey', 'mule'], 0, 0, 0, 0, '', False, 0, 0, 1.5, 1),
    ('pack_saddle', 'tack', 'saddle', ['donkey', 'mule'], 0, 0, 0, 0, '', False, 0, 5, 1.0, 0),
]
FIELDS = ['id', 'kind', 'slot', 'animals', 'defense', 'toughness', 'knockback', 'enchantability', 'repair', 'dyeable',
          'undyed', 'columns', 'bond_ride', 'calm']
NAMES = {'caparison': 'Caparison', 'leather_barding': 'Leather Barding', 'mail_barding': 'Mail Barding',
         'plate_barding': 'Plate Barding', 'saddlebags': 'Saddlebags', 'bridle': 'Bridle', 'pack_saddle': 'Pack Saddle'}

LANCE = {'id': 'jousting_lance', 'name': 'Jousting Lance', 'material': 'iron', 'attack_duration': 1.25, 'damage_multiplier': 1.6,
         'delay': 0.75, 'dismount_time': 3.0, 'dismount_threshold': 9.0, 'knockback_time': 8.0, 'knockback_threshold': 7.0,
         'damage_time': 10.0, 'damage_threshold': 7.0, 'reach': [2.0, 5.0, 2.0, 7.0, 0.125, 0.5]}


def table():
    rows = []
    for row in GEAR:
        g = dict(zip(FIELDS, row))
        assert g['kind'] in ('barding', 'tack') and g['slot'] == ('body' if g['kind'] == 'barding' else 'saddle'), g['id']
        assert set(g['animals']) <= {'horse', 'donkey', 'mule'} and 0 <= g['columns'] <= 5, g['id']
        rows.append(g)
    return {'gear': rows, 'lance': {k: v for k, v in LANCE.items() if k != 'name'}}


def outputs():
    # Equipment layers, textures, sprites and recipes are added here by the gear package.
    return {TABLES / 'gear.json': dump(table())}


def preview():
    print('gear: no art to preview yet.')
