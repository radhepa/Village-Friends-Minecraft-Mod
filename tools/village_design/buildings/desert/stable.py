"""Desert stable: the plains stable (``buildings/stable.py``) with smooth sandstone walls on cut-sandstone posts
under an acacia roof for shade, and a sandy yard. Its horses settle as desert horses."""
from ..stable import Materials, build
from .palette import ROOFS

DESERT = Materials(post='cut_sandstone', wall='smooth_sandstone', roof=ROOFS['acacia'], gable='smooth_sandstone', fence='acacia_fence',
                   floor=('sand', 'coarse_dirt', 'sand'), yard=('sand', 'sand', 'coarse_dirt'),
                   plant='dead_bush', log_post=False)


def stable():
    return build('desert/stable', DESERT, 614)


DESIGNS = {'desert/stable': stable}
