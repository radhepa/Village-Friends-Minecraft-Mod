"""Savanna village palette: an acacia frontier town.

Shared by every savanna design. Treat it as read-only; add local helpers to your
own module instead of editing it.

Art direction: acacia logs and planks with orange, white and brown terracotta,
packed mud and mud-brick walls, low wide roofs (acacia stairs, or thatch made of
hay bales and slabs) with deep eaves, open verandas on posts, woven fences
(acacia fence and gates), animal pens and drying racks. Accents of red and orange
banners and wool. Greenery: lone acacia trees, tall grass, coarse dirt yards.
"""
from ...roads import Theme, noise, smooth
from ...parts import Style, Roof

ROOFS = {
    'acacia': Roof('acacia_stairs', 'acacia_slab', 'acacia_planks'),
    'thatch': Roof('mud_brick_stairs', 'mud_brick_slab', 'hay_block'),
    'terracotta': Roof('granite_stairs', 'granite_slab', 'terracotta'),
    'dark': Roof('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks'),
}
STYLES = {
    'acacia': Style(frame='stripped_acacia_log', fill='orange_terracotta', floor='acacia_planks', roof=ROOFS['acacia'],
                    base='packed_mud', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
                    upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak'),
    'mud': Style(frame='acacia_log', fill='packed_mud', floor='acacia_planks', roof=ROOFS['dark'],
                 base='mud_bricks', base_stairs='mud_brick_stairs', trim='dark_oak', door='acacia',
                 upper_fill='packed_mud', ceiling='dark_oak_planks', accent='acacia'),
    'clay': Style(frame='stripped_acacia_log', fill='white_terracotta', floor='acacia_planks', roof=ROOFS['terracotta'],
                  base='brown_terracotta', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
                  upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak'),
}
LOOT = 'minecraft:chests/village/village_savanna_house'


def road(x, z, seed, centrality):
    n = smooth(x, z, seed) * 0.7 + noise(x, z, seed + 7) * 0.3
    v = n + centrality * 0.25
    if v > 0.86:
        return 'packed_mud'
    if v > 0.74:
        return 'gravel'
    if v < 0.2:
        return 'coarse_dirt'
    if noise(x, z, seed + 3) < 0.06:
        return 'red_sand'
    return 'dirt_path'


def edge(r):
    return 'coarse_dirt' if r < .45 else 'dirt_path' if r < .6 else 'grass_block'


THEME = Theme(prefix='savanna/', streets='savanna/streets', ends='savanna/street_ends', lots='savanna/lots',
              road=road, edge=edge, post='acacia_fence', post_base='packed_mud', light='lantern',
              planter='grass_block', bush='acacia_leaves', bush_alt='tall_grass', wood='acacia', stone='cobblestone',
              seed_offset=2000)
