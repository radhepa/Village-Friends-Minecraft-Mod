"""Import numbered name sections as data; document prose is never executed."""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'tools/name_pools.json'
TARGET = ROOT/'src/main/resources/data/villagefriends/villagefriends/names.json'
OLD_FIRST = 'Avery Rowan Milo Piper Jasper Hazel Finn Willow Theo Ivy Cedar Nora Leo Juniper Robin Sage Bram Clover Arlo Wren Otis Maple Ellis Lark'.split()
OLD_LAST = 'Meadow Oakridge Brook Fern Hill Greenfield Moss Sunvale Hearth Wheatley Riverbend Stonewell'.split()


def unique(values):
    return list(dict.fromkeys(v.strip() for v in values if v.strip()))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,help='Import a supplied markdown list; otherwise package the editable name_pools.json.')
    args=parser.parse_args()
    if args.source:
        sections={}
        for section in re.split(r'^## ',args.source.read_text(encoding='utf-8-sig'),flags=re.M)[1:]:
            title=section.splitlines()[0]
            sections[title.split(' ')[0]]=re.findall(r'^\s*\d+\.\s+(.+?)\s*$',section,flags=re.M)
        assert all(k in sections for k in ('Boys','Girls','Last','Indian','Chinese'))
        restricted=unique(sections['Indian']); blocked={n.casefold() for n in restricted}
        surnames=unique(sections['Last']+OLD_LAST)
        data={'version':1,'sourceRows':{k:len(v) for k,v in sections.items()},'pools':[
            {'id':'general','weight':80,'complexions':[0,1,2,3,4,5],
             'names':[n for n in unique(sections['Boys']+sections['Girls']+OLD_FIRST) if n.casefold() not in blocked]},
            {'id':'indian','weight':20,'complexions':[2,3,4,5],'names':restricted},
            {'id':'chinese','weight':15,'complexions':[0,1,2,3,4,5],
             'names':[n for n in unique(sections['Chinese']) if n.casefold() not in blocked]}],
            'surnames':[n for n in surnames if n.casefold() not in blocked],
            'restrictedSurnames':[n for n in surnames if n.casefold() in blocked],
            'restrictedSurnameComplexions':[2,3,4,5]}
        SOURCE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    TARGET.parent.mkdir(parents=True,exist_ok=True)
    TARGET.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Packaged name pools:',{p['id']:len(p['names']) for p in data['pools']},
          'surnames:',len(data['surnames'])+len(data['restrictedSurnames']))


if __name__=='__main__':main()
