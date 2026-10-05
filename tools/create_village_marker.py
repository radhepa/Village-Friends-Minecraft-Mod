"""Paint and package an original carved village marker, using vanilla block formats."""
from pathlib import Path
from PIL import Image, ImageDraw
import json
ROOT=Path(__file__).resolve().parent.parent/'src/main/resources'
def save(path,data):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
im=Image.new('RGBA',(16,16),'#B28453');d=ImageDraw.Draw(im)
d.rectangle((0,0,15,15),outline='#6B482E');d.line((1,1,14,1),fill='#D7B077');d.line((1,14,14,14),fill='#855735')
for y in (4,8,12):d.line((1,y,14,y),fill='#A17346')
for x,y in [(1,2),(14,2),(1,13),(14,13)]:d.point((x,y),fill='#C08651')
# An inset house and sprig: readable without tiny pretend text.
d.line([(4,6),(8,3),(12,6)],fill='#5C452F',width=2);d.rectangle((5,7,11,12),fill='#5C452F')
d.rectangle((7,9,9,12),fill='#D7B077');d.point((6,8),fill='#D7B077');d.point((10,8),fill='#D7B077')
d.line((2,9,2,12),fill='#58694B');d.point((3,9),fill='#65764E')
p=ROOT/'assets/villagefriends/textures/block/village_marker.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
def element(a,b,board=False):
    return {'from':a,'to':b,'faces':{f:{'texture':'#face' if board and f in ('north','south') else '#wood','uv':[0,0,16,16]} for f in ['down','up','north','south','east','west']}}
save(Path('assets/villagefriends/models/block/village_marker.json'),{
    'parent':'minecraft:block/block','textures':{'wood':'minecraft:block/stripped_oak_log','face':'villagefriends:block/village_marker','particle':'minecraft:block/stripped_oak_log'},
    'elements':[element([3,0,3],[13,3,13]),element([7,3,7],[9,10,9]),element([2,8,6],[14,16,10],True)],
    'display':{'gui':{'rotation':[30,225,0],'translation':[0,0,0],'scale':[.8,.8,.8]},'ground':{'translation':[0,3,0],'scale':[.4,.4,.4]},'fixed':{'scale':[.7,.7,.7]}}})
save(Path('assets/villagefriends/blockstates/village_marker.json'),{'variants':{'facing='+f:{'model':'villagefriends:block/village_marker','y':n} for f,n in [('north',0),('east',90),('south',180),('west',270)]}})
save(Path('assets/villagefriends/items/village_marker.json'),{'model':{'type':'minecraft:model','model':'villagefriends:block/village_marker'}})
language_path=ROOT/'assets/villagefriends/lang/en_us.json'
language=json.loads(language_path.read_text(encoding='utf-8')) if language_path.exists() else {}
language['block.villagefriends.village_marker']='Village Marker'
save(Path('assets/villagefriends/lang/en_us.json'),language)
save(Path('data/villagefriends/recipe/village_marker.json'),{'type':'minecraft:crafting_shaped','pattern':['PSP',' C ',' P '],
    'key':{'P':'#minecraft:planks','S':'minecraft:oak_sign','C':'minecraft:copper_ingot'},'result':{'id':'villagefriends:village_marker','count':1}})
save(Path('data/villagefriends/loot_table/blocks/village_marker.json'),{'type':'minecraft:block','pools':[{'rolls':1,'entries':[{'type':'minecraft:item','name':'villagefriends:village_marker'}],'conditions':[{'condition':'minecraft:survives_explosion'}]}]})
axe_path=ROOT/'data/minecraft/tags/block/mineable/axe.json'
axe=json.loads(axe_path.read_text(encoding='utf-8')) if axe_path.exists() else {'replace':False,'values':[]}
axe['values']=sorted(set(axe['values'])|{'villagefriends:village_marker'})
save(Path('data/minecraft/tags/block/mineable/axe.json'),axe)
save(Path('data/villagefriends/advancement/recipes/decorations/village_marker.json'),{'parent':'minecraft:recipes/root',
    'criteria':{'has_sign':{'trigger':'minecraft:inventory_changed','conditions':{'items':[{'items':'minecraft:oak_sign'}]}},'has_recipe':{'trigger':'minecraft:recipe_unlocked','conditions':{'recipes':'villagefriends:village_marker'}}},
    'requirements':[['has_sign','has_recipe']],'rewards':{'recipes':['villagefriends:village_marker']}})
print('Village Marker: carved board, directional block model, craft recipe, loot and recipe unlock.')
