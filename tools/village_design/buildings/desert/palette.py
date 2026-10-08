"""Desert village palette: a sun-baked oasis town.

Shared by every desert design. Treat it as read-only; add local helpers to your
own module instead of editing it.

Art direction: sandstone and smooth-sandstone walls with cut-sandstone trim,
terracotta accents (white, orange, yellow, red), flat roofs with parapets, a few
domes and stepped towers, striped wool awnings and acacia/jungle wood for doors,
lintels and lattice (trapdoor) windows. Shade matters: porches, arcades and
awnings. Greenery is concentrated around water: palms (jungle log + jungle
leaves), sugar cane along channels, cactus and dead bushes in yards.
"""
from ...roads import Theme, noise, smooth
from ...parts import Style, Roof

ROOFS = {
    'sandstone': Roof('smooth_sandstone_stairs', 'smooth_sandstone_slab', 'smooth_sandstone'),
    'cut': Roof('sandstone_stairs', 'cut_sandstone_slab', 'cut_sandstone'),
    'terracotta': Roof('granite_stairs', 'granite_slab', 'orange_terracotta'),
    'acacia': Roof('acacia_stairs', 'acacia_slab', 'acacia_planks'),
}
STYLES = {
    'sandstone': Style(frame='cut_sandstone', fill='smooth_sandstone', floor='sandstone', roof=ROOFS['sandstone'],
                       base='sandstone', base_stairs='sandstone_stairs', trim='acacia', door='acacia',
                       upper_fill='smooth_sandstone', ceiling='acacia_planks', accent='jungle'),
    'plaster': Style(frame='stripped_jungle_log', fill='white_terracotta', floor='smooth_sandstone',
                     roof=ROOFS['cut'], base='sandstone', base_stairs='sandstone_stairs', trim='jungle', door='jungle',
                     upper_fill='white_terracotta', ceiling='jungle_planks', accent='acacia'),
    'ochre': Style(frame='cut_sandstone', fill='yellow_terracotta', floor='smooth_sandstone', roof=ROOFS['terracotta'],
                   base='sandstone', base_stairs='sandstone_stairs', trim='acacia', door='acacia',
                   upper_fill='orange_terracotta', ceiling='acacia_planks', accent='jungle'),
}
AWNINGS = ('orange', 'white', 'red', 'yellow', 'cyan')
LOOT = 'minecraft:chests/village/village_desert_house'


def road(x, z, seed, centrality):
    n = smooth(x, z, seed) * 0.7 + noise(x, z, seed + 7) * 0.3
    v = n + centrality * 0.25
    if v > 0.84:
        return 'smooth_sandstone'
    if v > 0.72:
        return 'sandstone'
    if v > 0.66:
        return 'cut_sandstone'
    if v < 0.18:
        return 'sand'
    if noise(x, z, seed + 3) < 0.05:
        return 'gravel'
    return 'smooth_sandstone' if v > 0.5 else 'sandstone'


def edge(r):
    return 'sandstone' if r < .35 else 'sand'


THEME = Theme(prefix='desert/', streets='desert/streets', ends='desert/street_ends', lots='desert/lots',
              road=road, edge=edge, post='sandstone_wall', post_base='cut_sandstone', light='lantern',
              planter='sand', bush='dead_bush', bush_alt='cactus', wood='acacia', stone='sandstone', seed_offset=1000)
