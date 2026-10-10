"""Taiga stable: the plains stable (``buildings/stable.py``) in spruce logs and planks under a dark oak roof, with
a podzol yard. Its horses settle as the taiga's breeds (fjords, rounceys and draft horses)."""
from ..stable import Materials, build
from .palette import ROOFS

TAIGA = Materials(post='spruce_log', wall='spruce_planks', roof=ROOFS['dark_oak'], gable='spruce_planks', fence='spruce_fence',
                  floor=('coarse_dirt', 'podzol', 'rooted_dirt'), yard=('podzol', 'grass_block', 'coarse_dirt'),
                  plant='fern')


def stable():
    return build('taiga/stable', TAIGA, 613)


DESIGNS = {'taiga/stable': stable}
