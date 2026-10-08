"""Snowy village palette: a frost hamlet.

Shared by every snowy design. Treat it as read-only; add local helpers to your
own module instead of editing it.

Art direction: heavy spruce log and plank houses on stone-brick and cobblestone
plinths, steep roofs (pitch 2) in spruce, dark oak or deepslate tiles that will
gather snow, big stone chimneys with smoke on almost every building, small
windows, enclosed porches, warm lantern light, woodpiles under eaves, sledges and
ice-fishing huts. Accents of packed and blue ice, white and light-blue wool.
Greenery: spruce trees and spruce-leaf bushes; snow covers the rest naturally.
"""
from ...roads import Theme, noise, smooth
from ...parts import Style, Roof

ROOFS = {
    'spruce': Roof('spruce_stairs', 'spruce_slab', 'spruce_planks'),
    'dark_oak': Roof('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks'),
    'slate': Roof('deepslate_tile_stairs', 'deepslate_tile_slab', 'deepslate_tiles'),
    'stone': Roof('stone_brick_stairs', 'stone_brick_slab', 'stone_bricks'),
}
STYLES = {
    'cabin': Style(frame='spruce_log', fill='spruce_planks', floor='spruce_planks', roof=ROOFS['dark_oak'],
                   base='cobblestone', base_stairs='cobblestone_stairs', trim='spruce', door='spruce',
                   upper_fill='stripped_spruce_log', ceiling='spruce_planks', accent='dark_oak'),
    'stone': Style(frame='stripped_spruce_log', fill='stone_bricks', floor='spruce_planks', roof=ROOFS['slate'],
                   base='cobblestone', base_stairs='cobblestone_stairs', trim='spruce', door='spruce',
                   upper_fill='spruce_planks', ceiling='spruce_planks', accent='dark_oak'),
    'white': Style(frame='spruce_log', fill='white_terracotta', floor='spruce_planks', roof=ROOFS['spruce'],
                   base='stone_bricks', base_stairs='stone_brick_stairs', trim='dark_oak', door='dark_oak',
                   upper_fill='white_terracotta', ceiling='dark_oak_planks', accent='spruce'),
}
LOOT = 'minecraft:chests/village/village_snowy_house'


def road(x, z, seed, centrality):
    n = smooth(x, z, seed) * 0.7 + noise(x, z, seed + 7) * 0.3
    v = n + centrality * 0.25
    if v > 0.84:
        return 'cobblestone'
    if v > 0.7:
        return 'gravel'
    if v < 0.2:
        return 'snow_block'
    if noise(x, z, seed + 3) < 0.05:
        return 'packed_ice'
    return 'dirt_path'


def edge(r):
    return 'snow_block' if r < .5 else 'gravel' if r < .6 else 'grass_block'


THEME = Theme(prefix='snowy/', streets='snowy/streets', ends='snowy/street_ends', lots='snowy/lots',
              road=road, edge=edge, post='spruce_fence', post_base='cobblestone', light='lantern',
              planter='grass_block', bush='spruce_leaves', bush_alt='spruce_leaves', wood='spruce',
              stone='cobblestone', seed_offset=3000)
