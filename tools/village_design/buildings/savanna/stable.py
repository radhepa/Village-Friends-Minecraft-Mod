"""Savanna stable: the plains stable (``buildings/stable.py``) in acacia, under a deep acacia roof, with a
coarse-dirt yard behind a woven acacia fence. Its horses settle as the savanna's breeds (coursers and steppe ponies)."""
from ..stable import Materials, build
from .palette import ROOFS

SAVANNA = Materials(post='stripped_acacia_log', wall='acacia_planks', roof=ROOFS['acacia'], gable='orange_terracotta', fence='acacia_fence',
                    gate='acacia_fence_gate', floor=('coarse_dirt', 'packed_mud', 'coarse_dirt'), yard=('coarse_dirt', 'grass_block', 'grass_block'),
                    plant='short_grass')


def stable():
    return build('savanna/stable', SAVANNA, 612)


DESIGNS = {'savanna/stable': stable}
