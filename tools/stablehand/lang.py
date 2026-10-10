"""Stablehand's names in the language file, and the stablehand's job site in vanilla's acquirable job sites
(so an unemployed resident next to a Saddle Rack can take the job).

Both are merges: every other key and tag value stays as it is. Everything else players read in Stablehand
is plain text in the Java code. Breed names come from the breed table.
"""
from breeds import BREEDS
from gear import LANCE, NAMES as GEAR_NAMES
from kit import DATA, LANG, NS, merge_tag, merged_lang

ITEMS = {'grooming_brush': 'Grooming Brush', 'horse_whistle': 'Horse Whistle', 'horse_papers': 'Horse Papers',
         **GEAR_NAMES, LANCE['id']: LANCE['name']}
BLOCKS = {'horse_stall': 'Horse Stall', 'hay_trough': 'Hay Trough', 'saddle_rack': 'Saddle Rack'}
BOND_TIERS = ['Wary', 'Familiar', 'Trusting', 'Loyal', 'Devoted']
JOB_SITES = DATA / 'minecraft/tags/point_of_interest_type/acquirable_job_site.json'


def names():
    out = {f'item.{NS}.{k}': v for k, v in ITEMS.items()}
    out.update({f'block.{NS}.{k}': v for k, v in BLOCKS.items()})
    out[f'entity.{NS}.villager.stablehand'] = 'Stablehand'
    out.update({f'stablehand.breed.{b["id"]}': b['name'] for b in BREEDS})
    out['stablehand.breed.donkey'] = 'Donkey'
    out['stablehand.breed.mule'] = 'Mule'
    out.update({f'stablehand.bond.{i}': t for i, t in enumerate(BOND_TIERS)})
    return out


def outputs():
    return {LANG: merged_lang(names()), JOB_SITES: merge_tag(JOB_SITES, [f'{NS}:stablehand'])}


def preview():
    print('lang: nothing to preview.')
