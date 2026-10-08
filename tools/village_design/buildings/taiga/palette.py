"""Taiga village palette: a forest lodge village.

Shared by every taiga design. Treat it as read-only; add local helpers to your
own module instead of editing it.

Art direction: true log cabins (horizontal spruce logs with crossed corners),
dark oak and spruce framing, mossy cobblestone and stone foundations, steep
spruce or dark-oak roofs with moss carpet patches, porches with log posts,
lantern light, hunting and logging details (drying racks, chopping blocks, log
stacks, barrels), sweet berry bushes, pumpkins and podzol yards. Accents of
green and brown wool and banners.
"""
from ...roads import Theme, noise, smooth
from ...parts import Style, Roof

ROOFS = {
    'spruce': Roof('spruce_stairs', 'spruce_slab', 'spruce_planks'),
    'dark_oak': Roof('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks'),
    'mossy': Roof('mossy_cobblestone_stairs', 'mossy_cobblestone_slab', 'mossy_cobblestone'),
}
STYLES = {
    'log': Style(frame='spruce_log', fill='stripped_spruce_log', floor='spruce_planks', roof=ROOFS['dark_oak'],
                 base='mossy_cobblestone', base_stairs='mossy_cobblestone_stairs', trim='spruce', door='spruce',
                 upper_fill='spruce_planks', ceiling='spruce_planks', accent='dark_oak'),
    'dark': Style(frame='dark_oak_log', fill='spruce_planks', floor='dark_oak_planks', roof=ROOFS['spruce'],
                  base='cobblestone', base_stairs='cobblestone_stairs', trim='dark_oak', door='dark_oak',
                  upper_fill='spruce_planks', ceiling='dark_oak_planks', accent='spruce'),
    'stone': Style(frame='stripped_dark_oak_log', fill='cobblestone', floor='spruce_planks', roof=ROOFS['spruce'],
                   base='mossy_stone_bricks', base_stairs='stone_brick_stairs', trim='spruce', door='spruce',
                   upper_fill='stripped_spruce_log', ceiling='spruce_planks', accent='dark_oak'),
}
LOOT = 'minecraft:chests/village/village_taiga_house'


def road(x, z, seed, centrality):
    n = smooth(x, z, seed) * 0.7 + noise(x, z, seed + 7) * 0.3
    v = n + centrality * 0.25
    if v > 0.86:
        return 'mossy_cobblestone'
    if v > 0.76:
        return 'cobblestone'
    if v > 0.7:
        return 'gravel'
    if v < 0.2:
        return 'podzol'
    if noise(x, z, seed + 3) < 0.08:
        return 'coarse_dirt'
    return 'dirt_path'


def edge(r):
    return 'podzol' if r < .35 else 'coarse_dirt' if r < .55 else 'grass_block'


THEME = Theme(prefix='taiga/', streets='taiga/streets', ends='taiga/street_ends', lots='taiga/lots',
              road=road, edge=edge, post='spruce_fence', post_base='mossy_cobblestone', light='lantern',
              planter='podzol', bush='spruce_leaves', bush_alt='sweet_berry_bush', wood='spruce',
              stone='cobblestone', seed_offset=4000)
