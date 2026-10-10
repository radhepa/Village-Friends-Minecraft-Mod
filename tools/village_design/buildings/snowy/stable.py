"""Snowy stable: the plains stable (``buildings/stable.py``) in spruce under a steep roof that gathers snow. Its
horses settle as the snowy villages' breeds (fjords and draft horses)."""
from ..stable import Materials, build
from .palette import ROOFS

SNOWY = Materials(post='spruce_log', wall='spruce_planks', roof=ROOFS['spruce'], gable='spruce_planks', fence='spruce_fence',
                  gate='spruce_fence_gate', floor=('coarse_dirt', 'packed_mud', 'rooted_dirt'), yard=('grass_block',), pitch=2)


def stable():
    return build('snowy/stable', SNOWY, 615)


DESIGNS = {'snowy/stable': stable}
