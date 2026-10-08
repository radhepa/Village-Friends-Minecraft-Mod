# Wardrobe backlog

These outfit batches were planned for the 2.14 wardrobe expansion but not built yet. Each one keeps the numbers reserved for it, so a later batch fills its gap in the sequence:

| Batch | Theme | Men's ids | Women's ids |
|---|---|---|---|
| m02 | Craft guilds and workshops | t146-t170, b146-b170 | |
| m06 | Nobles, court and town officials | t246-t270, b246-b270 | |
| m09 | Festivals, seasons and ceremony | t321-t345, b321-b345 | |
| f02 | Crafts and trades | | tf086-tf110, bf086-bf110 |
| f06 | Noble court and town | | tf186-tf210, bf186-bf210 |
| f08 | The wider medieval world | | tf236-tf260, bf236-bf260 |
| f09 | Festivals, ceremony and seasons | | tf261-tf285, bf261-bf285 |

Shared helper kits were started for m02, m06, f02 and f06 (`kit_m02.py` and the others in this folder). To start one of those batches, move its kit to `tools/wardrobe/`. The compiler only reads pieces from `hair/`, `tops/` and `bottoms/`, so nothing in this folder is built.

When a batch is done, update the wardrobe counts in `WardrobeTest`, `OUTFIT_ENGINE.md` and the changelog.

# Concepts

Each line is one outfit: `number | top | bottom | professions | notes`. **[locked]** marks a set that is designed as one outfit; every other line mixes freely. Seeds are noise seeds for the textures; use the batch's own range.

## m02: Men, craft guilds and workshops (t/b 146–170). Seeds 32000–32999. Outfit file male_m02.json
146 | Glassblower's Scorch-Sleeved Smock | Glasshouse Leather Leggings | TOOLSMITH, ARMORER | blowpipe, scorched sleeves
147 | Wheelwright's Spokeshave Apron | Wheelwright's Patched Breeches | CARPENTER, TOOLSMITH | spokeshave in apron loop
148 | Cobbler's Lapstone Apron | Cobbler's Own Fine Boots | LEATHERWORKER | lapstone and last on the apron
149 | Bookbinder's Thread-Spool Waistcoat | Bookbinder's Press Trousers | LIBRARIAN, LEATHERWORKER | thread spools on a cord
150 | Ropemaker's Twisted-Hemp Jerkin | Rope Walk Trousers | FISHERMAN, NONE | coils of rope over a shoulder
151 | Fuller's Wet-Shrunk Tunic | Fulling-Trough Bare Legs | TAILOR, SHEPHERD | kilted tunic, wet bare legs
152 | Bowyer's Stave-Wrapped Vest | Bowyer's Bowstring-Garter Hose | FLETCHER, ARCHER | unstrung stave across the back
153 | Locksmith's Key-Ring Jerkin | Locksmith's Tool-Roll Trousers | TOOLSMITH | big key ring at the hip
154 | Bell Founder's Bronze-Burnt Smock | Casting-Pit Hobnail Boots | TOOLSMITH, ARMORER | small bell on the belt
155 | Pewterer's Polished Apron | Pewterer's Button-Knee Breeches | TOOLSMITH | metal-bright apron studs
156 | Saddler's Stitching-Palm Jerkin | Saddler's Riding Leathers | LEATHERWORKER | sewing palm, girth straps
157 | Glover's Fitted Doublet | Glover's Soft Kid Hose | LEATHERWORKER, TAILOR | pair of gloves tucked at the belt
158 | Basket Weaver's Willow-Strapped Tunic | Osier-Bed Wading Trousers | NONE, FARMER | willow bundle, basket on back
159 | Lime Burner's Ash-White Smock | Lime-Kiln Clogs and Wraps | MASON | chalky white dust
160 | Roof Tiler's Kneeling-Pad Tunic | Roof Tiler's Strapped Knee Boots | MASON, CARPENTER | tile hod on shoulder
161 | Joiner's Shaving-Curl Apron | Joiner's Rule-Pocket Trousers | CARPENTER | wood shavings, folding rule
162 | Wood Turner's Lathe Smock | Turner's Treadle Boots | CARPENTER, TOOLSMITH | turned bowl at the belt
163 | Cutler's Blade-Belt Jerkin | Cutler's Spark-Burnt Leggings | WEAPONSMITH, TOOLSMITH | sheathed knives on a belt
164 | Weaver's Shuttle-Pocket Tunic | Weaver's Treadle Hose | TAILOR, SHEPHERD | shuttle in breast pocket
165 | Dyer's Woad-Blue Smock | Dye-Vat Rolled Trousers | TAILOR, PAINTER | dye-stained forearms
166 | Hatter's Steam-Pressed Coat | Hatter's Narrow Hose | TAILOR, NITWIT | hat blocks hung at hip
167 | Soap Boiler's Lye-Spotted Smock | Soap Boiler's Wooden Pattens | APOTHECARY, COOK | stirring paddle
168 | Parchment Maker's Scraper Apron | Parchment Maker's Hide Leggings | LIBRARIAN, LEATHERWORKER | lunellum scraper
169 | Clockmaker's Gear-Fob Waistcoat | Clockmaker's Fine Knee Hose | TOOLSMITH, SCHOLAR | gear-wheel fob, loupe
170 | Armourer's Apprentice Quilted Bib | Apprentice's Spark-Pocked Trousers | ARMORER | quilted bib, tongs

## m06: Men, nobles, court and town officials (t/b 246–270). Seeds 36000–36999. Outfit file male_m06.json
246 | Mayor's Chain-of-Office Robe | Mayor's Fur-Hemmed Hose | LIBRARIAN, TAVERN_KEEPER, MERCHANT | heavy chain of office
247 | Alderman's Scarlet Gown | Alderman's Buckled Shoes and Hose | CLERIC, MERCHANT | long scarlet gown
248 | Guildmaster's Badge Doublet | Guildmaster's Paned Trunk Hose | TAILOR, TOOLSMITH, MERCHANT | guild badge
249 | Bailiff's Staff-Belt Coat | Bailiff's Riding Gaiters | GUARD, FARMER | staff of office
250 | Steward's Keys and Purse Doublet | Steward's Fine Hose | TAVERN_KEEPER, LIBRARIAN, MERCHANT | purse and keys
251 | Chamberlain's Embroidered Robe | Chamberlain's Slippers | CLERIC, TAILOR | key of office on ribbon
252 | Sheriff's Badge Mantle | Sheriff's Riding Boots | GUARD, KNIGHT | short mantle, badge
253 | Tax Collector's Coin-Satchel Coat | Tax Collector's Pinched Hose | NITWIT, MERCHANT | coin satchel, tally stick
254 | Page's Quartered Tabard | Page's Parti Hose | KNIGHT, BARD | small quartered tabard
255 | Courtier's Padded-Shoulder Doublet | Courtier's Pumpkin Breeches | TAILOR, BARD, PAINTER | puffed paned breeches
256 | Young Prince's Velvet Gown | Prince's Soft Boots | KNIGHT, TAILOR | gilt belt
257 | Baron's Ermine-Collar Surcoat | Baron's Spurred Boots | KNIGHT | ermine spots
258 | Envoy's Sealed-Letter Tabard | Envoy's Travel Hose | CARTOGRAPHER, MERCHANT | letter case, seal
259 | Master of Hounds' Horn-Baldric Coat | Huntsman's Thigh Boots | FLETCHER, ARCHER | hunting horn on baldric
260 | Cupbearer's Silk Tunic | Cupbearer's Slashed Hose | TAVERN_KEEPER, COOK | goblet at belt
261 | Moneychanger's Scale-Hung Robe | Moneychanger's Velvet Slippers | LIBRARIAN, MERCHANT | small balance scale
262 | Wool Merchant's Fleece-Seal Gown | Wool Merchant's Riding Boots | SHEPHERD, MERCHANT | wool sack seal
263 | Cloth Merchant's Swatch Coat | Cloth Merchant's Fine Hose | TAILOR, MERCHANT | bolt of cloth, swatches
264 | Burgess's Short Pleated Jacket | Burgess's Two-Tone Hose | TAVERN_KEEPER, NONE, MERCHANT | pleated skirted jacket
265 | Pursuivant's Small Tabard | Pursuivant's Riding Hose | BARD, KNIGHT | tabard worn sideways (a pursuivant's way)
266 | Lord's Hunting Jacket | Lord's Hunting Boots | ARCHER, KNIGHT | slung crossbow
267 | Seneschal's Long Brocade Gown | Seneschal's Train Hem | LIBRARIAN, CLERIC | [locked]
268 | Knight's Leisure Cote | Knight's Spurred Court Hose | KNIGHT | unarmored court dress, belt of knighthood
269 | Court Dancer's Dagged Tunic | Dancer's Long-Toed Hose | BARD, NITWIT | dagged sleeves
270 | Gentry Youth's Hanging-Sleeve Cotte | Gentry Youth's Poulaine Hose | BARD, TAILOR, NONE | short cotte

## m09: Men, festivals, seasons and ceremony (t/b 321–345). Seeds 39000–39999. Outfit file male_m09.json
321 | Harvest Home Ribboned Smock | Harvest Home Wheat-Tied Gaiters | FARMER, BARD | ribbons, wheat ears
322 | Midsummer Bonfire Tunic | Midsummer Ribboned Trousers | NONE, BARD | flame embroidery
323 | Yuletide Holly-Trimmed Coat | Yule Log Bearer's Boots | NONE, COOK, TAVERN_KEEPER | holly sprig and berries
324 | Wedding Guest's Best Doublet | Wedding Guest's Polished Shoes and Hose | NONE, TAILOR | flower buttonhole
325 | Mourning Gown with Weepers | Mourning Hose | CLERIC, NONE | black, hanging weeper sleeves
326 | Feast-Day Best Tunic | Feast-Day Hose | NONE, NITWIT | clean, bright borders
327 | Wassailer's Bowl-Bearing Tunic | Wassailer's Ribbon Garters | TAVERN_KEEPER, BARD | wassail bowl
328 | Plough Monday Straw-Sash Smock | Plough Monday Bell Gaiters | FARMER | straw sash
329 | Carnival Mask-Seller's Coat | Carnival Diamond Hose | NITWIT, PAINTER, BARD | masks hanging on coat
330 | Saint's Day Procession Tabard | Procession Candle-Bearer's Robe Skirt | CLERIC | [locked]
331 | Lantern Night Lantern-Pole Coat | Lantern Night Soft Boots | NONE, NITWIT | lantern pole over shoulder
332 | Sword Dancer's Sashed Shirt | Sword Dancer's Kilted Breeches | BARD | crossed sashes
333 | Hobby Horse Rider's Ribboned Coat | Hobby Horse Frame | NITWIT, BARD | [locked] hobby-horse frame around the waist (head and tail)
334 | Boy Bishop's Mock Cope | Boy Bishop's Lace-Hem Alb | NITWIT, CLERIC | [locked] Feast of Fools
335 | Archery Champion's Sash Tunic | Champion's Arrow-Garter Hose | ARCHER, FLETCHER | silver arrow prize
336 | Mystery Play Angel's Wings and Alb | Angel's Alb Skirt | BARD, CLERIC, NITWIT | [locked] feathered wings on the back
337 | Mystery Play Devil's Tailed Coat | Devil's Shaggy Leggings | BARD, NITWIT | [locked] tail, shaggy legs
338 | Coronation Day Best Coat | Coronation Day Striped Hose | NONE, MERCHANT | bunting colors
339 | Spring Blossom Garland Tunic | Blossom-Strewn Hose | FARMER, BARD, NONE | flower garland
340 | Winter Solstice Fur Mantle | Solstice Fur-Wrapped Boots | CLERIC, NONE | sun brooch
341 | Fair Day Strongman's Leather Harness | Strongman's Striped Breeches | NONE, BUTCHER | bare arms, harness
342 | Fair Day Juggler's Ball-Pouch Tunic | Juggler's Tumbling Hose | NITWIT, BARD | ball pouches
343 | Puppeteer's Marionette Coat | Puppeteer's Stage-Hem Trousers | BARD, PAINTER | marionette hanging from hand bar
344 | Village Elder's Feast Robe | Elder's Fur-Lined Slippers | NONE, CLERIC | long robe, walking stick
345 | First Snow Sledder's Quilted Coat | Sledder's Strapped Snow Boots | NONE, NITWIT | sled rope

## f02: Women, crafts and trades (tf/bf 086–110). Seeds 52000–52999. Outfit file female_f02.json
086 | Lacemaker's Pillow Bodice | Lacemaker's Bobbin-Hung Skirt | TAILOR | lace pillow at waist, bobbins
087 | Embroiderer's Hoop-Hung Kirtle | Embroiderer's Thread-Hem Skirt | TAILOR, PAINTER | small hoop on ribbon
088 | Glover's Kidskin Bodice | Glover's Pinked-Hem Skirt | LEATHERWORKER, TAILOR | gloves at girdle
089 | Silkwoman's Spindle Bodice | Silkwoman's Sheen Skirt | TAILOR, MERCHANT | silk sheen
090 | Candlewife's Dipping-Rod Apron | Candlewife's Wax-Drip Skirt | CLERIC, APOTHECARY | candles on a rod
091 | Soap Maker's Lye Apron Bodice | Soap Maker's Pattened Skirt | APOTHECARY, COOK
092 | Glass Bead Maker's Bodice | Bead Maker's Bead-Strung Skirt | TOOLSMITH, TAILOR | beads strung along hem
093 | Bookbinder's Thread Waistcoat | Binder's Paste-Pot Skirt | LIBRARIAN | paste pot, bone folder
094 | Ropewalker's Hemp-Waist Bodice | Ropewalk Short Skirt and Hose | FISHERMAN, NONE | hemp around waist
095 | Basket Weaver's Willow Bodice | Basket Weaver's Osier Skirt | FARMER, NONE | basket on hip
096 | Girdler's Belt-Sample Bodice | Girdler's Hanging-Belts Skirt | LEATHERWORKER, TAILOR | many belts
097 | Pin Maker's Pincushion Bodice | Pin Maker's Tiny-Pocket Skirt | TAILOR, TOOLSMITH | pincushion on wrist
098 | Comb Maker's Horn Bodice | Comb Maker's Sawdust Skirt | CARPENTER, TOOLSMITH | combs at girdle
099 | Seamstress's Tape-Draped Kirtle | Seamstress's Pin-Hemmed Skirt | TAILOR | measuring tape over shoulders, shears
100 | Felt Maker's Rolled-Felt Bodice | Felt Maker's Felted Skirt | TAILOR, SHEPHERD
101 | Cooper's Wife's Stave Apron | Cooper's Wife's Hooped Skirt | CARPENTER | barrel hoops
102 | Tile Painter's Glaze-Spotted Smock | Tile Painter's Kiln Skirt | PAINTER, MASON | glazed tiles on belt
103 | Wood Carver's Chisel Bodice | Wood Carver's Shavings Skirt | CARPENTER | chisel roll
104 | Tapestry Weaver's Bobbin Bodice | Tapestry Weaver's Pictured Skirt | TAILOR, PAINTER | woven-scene band on hem
105 | Mirror Maker's Silvered Bodice | Mirror Maker's Gleam Skirt | TOOLSMITH, MERCHANT | small hand mirror
106 | Parchment Maker's Scraping Apron | Parchment Maker's Leather-Panel Skirt | LIBRARIAN, LEATHERWORKER
107 | Bell Founder's Daughter's Bronze Apron | Founder's Spark-Burnt Breeches | TOOLSMITH, ARMORER
108 | Saddler's Wife's Stitch-Belt Jerkin | Saddler's Riding Skirt | LEATHERWORKER
109 | Cordwainer's Shoe-Last Apron | Cordwainer's Fine Shoes and Skirt | LEATHERWORKER
110 | Bowstring Maker's Hemp-Wound Bodice | Bowstring Maker's Wound Skirt | FLETCHER, ARCHER

## f06: Women, noble court and town (tf/bf 186–210). Seeds 56000–56999. Outfit file female_f06.json
186 | Burgher Wife's Keys and Purse Bodice | Burgher Wife's Fur-Hem Skirt | TAVERN_KEEPER, NONE, MERCHANT
187 | Guild Mistress's Badge Gown | Guild Mistress's Brocade Skirt | TAILOR, MERCHANT
188 | Mayoress's Chain Bodice | Mayoress's Velvet Skirt | LIBRARIAN, MERCHANT
189 | Countess's Jewelled-Girdle Gown | Countess's Trailing Skirt | TAILOR, KNIGHT
190 | Princess's Tower-Embroidered Bodice | Princess's Star-Train Skirt | BARD, TAILOR
191 | Lady-in-Waiting's Ribboned Bodice | Lady-in-Waiting's Pleated Skirt | TAILOR, BARD
192 | Chatelaine's Key-Chain Bodice | Chatelaine's Practical Fine Skirt | TAVERN_KEEPER, LIBRARIAN
193 | Duchess's Cut-Velvet Gown | Duchess's Cut-Velvet Skirt | TAILOR, MERCHANT | [locked]
194 | Hawking Party Short Mantle | Hawking Party Skirt and Boots | ARCHER, KNIGHT
195 | Court Musician's Harp-Slung Bodice | Court Musician's Silk Skirt | BARD | small harp on back
196 | Envoy's Sealed-Letter Tabard | Envoy's Travel Skirt | CARTOGRAPHER, MERCHANT
197 | Merchant's Wife's Tablet-Woven Bodice | Merchant's Wife's Bordered Skirt | TAILOR, MERCHANT
198 | Moneylender's Scale Bodice | Moneylender's Purse-Hung Skirt | LIBRARIAN, MERCHANT
199 | Cloth Merchant's Swatch Kirtle | Cloth Merchant's Sample-Panel Skirt | TAILOR, MERCHANT
200 | Widow's Weeds Black Gown | Widow's Black Skirt | CLERIC, NONE | [locked]
201 | Heiress's Pearl-Buttoned Bodice | Heiress's Embroidered-Hem Skirt | TAILOR
202 | Debutante's Rosette Bodice | Debutante's Tiered Silk Skirt | BARD, NONE
203 | Lady Steward's Ledger-Belt Kirtle | Lady Steward's Sober Skirt | LIBRARIAN, MERCHANT
204 | Gentry Girl's Hanging-Sleeve Cotte | Gentry Girl's Narrow Skirt | NONE, BARD
205 | Lady of the Manor's Garden Gown | Lady of the Manor's Garden Skirt | FARMER, APOTHECARY
206 | Dowager's Fur-Lined Robe | Dowager's Heavy Skirt | CLERIC, LIBRARIAN
207 | Tournament Lady's Favour-Sleeve Gown | Tournament Lady's Banner Skirt | KNIGHT, BARD | one sleeve detached as a favour
208 | Court Painter's Velvet Smock | Court Painter's Daubed Silk Skirt | PAINTER
209 | Courtly Dancer's Trailing-Sleeve Bodice | Courtly Dancer's Swirl Skirt | BARD
210 | Lady Treasurer's Coffer-Key Gown | Lady Treasurer's Coin-Hem Skirt | LIBRARIAN, MERCHANT

## f08: Women, the wider medieval world (tf/bf 236–260). Seeds 58000–58999. Outfit file female_f08.json
Respectful, grounded, period-accurate silhouettes.
236 | Byzantine Clavi Dalmatica | Byzantine Pearl-Hem Skirt | MERCHANT, CLERIC
237 | Andalusian Silk Qamis | Andalusian Saraweel and Slippers | MERCHANT, APOTHECARY
238 | Persian Pirahan Robe | Persian Embroidered Trousers | MERCHANT, SCHOLAR, BARD
239 | Rus Sarafan | Rus Embroidered Rubakha Hem | NONE, FARMER | [locked]
240 | Polish Embroidered Bodice | Polish Striped Wool Skirt | NONE, BARD
241 | Hungarian Pleated-Apron Bodice | Hungarian Many-Petticoat Skirt | NONE, BARD
242 | Basque Shepherdess's Wool Jacket | Basque Abarka and Skirt | SHEPHERD
243 | Welsh Flannel Shawl Bodice | Welsh Striped Flannel Petticoat | NONE, SHEPHERD
244 | Irish Brat-Cloaked Leine | Irish Leine Skirt | NONE, BARD
245 | Breton Embroidered Bodice | Breton Velvet-Banded Skirt | FISHERMAN, NONE
246 | Sicilian Striped Market Bodice | Sicilian Fringed Shawl Skirt | MERCHANT, FARMER
247 | Venetian Cioppa Gown | Venetian Brocade Skirt | MERCHANT, TAILOR
248 | Alpine Dairywoman's Laced Bodice | Alpine Gathered Skirt and Apron | FARMER, COOK
249 | Bohemian Embroidered Blouse | Bohemian Pleated Skirt | NONE, BARD
250 | Northern Banded Gakti Dress | Northern Reindeer-Skin Boots and Skirt | SHEPHERD
251 | Steppe Noblewoman's Deel | Steppe Noblewoman's Riding Boots | SHEPHERD, ARCHER
252 | Song Ruqun Jacket | Song Pleated Ruqun Skirt | SCHOLAR, PAINTER, BARD
253 | Kosode Robe with Obi | Kosode Hakama | NONE, BARD, CLERIC
254 | Goryeo Short Jeogori | Goryeo High-Waist Chima | NONE, PAINTER
255 | Deccan Choli and Odhani | Deccan Lehenga Skirt | BARD, MERCHANT
256 | Ethiopian Habesha Kemis | Ethiopian Tibeb-Border Skirt | CLERIC, NONE
257 | Malian Indigo Boubou | Malian Wrapped Pagne | MERCHANT, BARD
258 | Berber Woven Haik Wrap | Berber Fibula-Pinned Skirt | SHEPHERD, NONE
259 | Anatolian Entari | Anatolian Shalvar Trousers | NONE, COOK
260 | Georgian Kartuli Gown | Georgian Trailing Skirt | BARD, NONE

## f09: Women, festivals, ceremony and seasons (tf/bf 261–285). Seeds 59000–59999. Outfit file female_f09.json
261 | Harvest Queen's Sheaf-Sash Bodice | Harvest Queen's Golden-Hem Skirt | FARMER, BARD
262 | Midsummer Fire-Dancer's Bodice | Midsummer Ribbon Skirt | BARD, NONE
263 | Yuletide Holly Bodice | Yuletide Velvet Skirt | NONE, COOK, TAVERN_KEEPER
264 | Village Bride's Wedding Kirtle | Village Bride's Wedding Skirt | NONE, TAILOR | [locked]
265 | Bridesmaid's Flower-Garland Bodice | Bridesmaid's Ribbon Skirt | NONE, BARD
266 | Feast-Day Best Kirtle | Feast-Day Best Skirt | NONE, NITWIT
267 | Carnival Mask-Seller's Coat | Carnival Diamond Skirt | NITWIT, PAINTER
268 | Lantern Festival Lantern-Pole Mantle | Lantern Festival Glow Skirt | NONE, CLERIC
269 | Saint's Day Procession Mantle | Procession Candle Skirt | CLERIC
270 | Wassail Maiden's Bowl Bodice | Wassail Maiden's Holly Skirt | TAVERN_KEEPER, BARD
271 | Spring Blossom Bodice | Spring Blossom Skirt | FARMER, NONE
272 | Winter Solstice Fur Shawl | Winter Solstice Sun-Embroidered Skirt | CLERIC, NONE
273 | Masque Ball Domino Cloak | Masque Ball Brocade Skirt | BARD, PAINTER
274 | Mystery Play Angel's Wings and Alb | Angel's Alb Skirt | CLERIC, BARD | [locked]
275 | Ribbon Dancer's Streamer Bodice | Ribbon Dancer's Twirl Skirt | BARD, NITWIT
276 | Sword Dancer's Sashed Bodice | Sword Dancer's Kilted Skirt | BARD
277 | Fair Day Acrobat's Tumbler Top | Acrobat's Tumbling Hose | NITWIT, BARD
278 | Puppeteer's Marionette Bodice | Puppeteer's Curtain Skirt | BARD, PAINTER
279 | Archery Winner's Sash Bodice | Archery Winner's Garter Skirt | ARCHER, FLETCHER
280 | Candlemas Candle-Bearer's White Bodice | Candlemas White Skirt | CLERIC, NONE
281 | Goose Fair Bodice | Goose Fair Striped Skirt | FARMER, MERCHANT
282 | Plough Monday Straw-Sash Bodice | Plough Monday Bell Skirt | FARMER
283 | Frost Fair Skater's Fur Jacket | Frost Fair Skating Skirt and Bone Skates | NONE, NITWIT
284 | Twelfth Night Bean Queen's Bodice | Twelfth Night Starred Skirt | NONE, TAVERN_KEEPER
285 | Hobby Horse Rider's Ribboned Bodice | Hobby Horse Frame Skirt | NITWIT, BARD | [locked]

# How a batch is built

Each batch is 25 outfits, meaning 25 tops and 25 bottoms. Build each batch in its own git worktree and branch, and don't push from there.

## Read first, in this order

1. `WARDROBE_EDITING.md` and `OUTFIT_ENGINE.md`.
2. `tools/wardrobe/kit.py` and `tools/wardrobe/paint.py`.
3. For men: `kit_male.py` and `kit_casual.py`. For women: `kit_female.py`.
4. At least **8 existing modules** of your gender: tops and bottoms, simple and elaborate. For example, men: `t11`, `t21`, `t45`, `t63`, `t72`, `t85`, `t93`, `b13`, `b22`, `b44`, `b78`, `b87`. Women: `tf001`, `tf009`, `tf019`, `tf030`, `tf041`, `tf052`, `tf056`, `bf001`, `bf017`, `bf030`, `bf041`, `bf055`.
5. Look at how they use `g.part`, `g.piece`, layering depths, motions (`flap_front`/`flap_back`/`sway`), tags, `requires`/`rejects` and `locked_to`.

## What to build

For each line of your batch, write one top module and one bottom module.

- Men: `tools/wardrobe/tops/tNNN_snake_name.py` and `tools/wardrobe/bottoms/bNNN_snake_name.py`.
- Women: `tools/wardrobe/tops/tfNNN_snake_name.py` and `tools/wardrobe/bottoms/bfNNN_snake_name.py`, with three-digit numbers.

Use exactly the numbers reserved for the batch. The file stem is the id: lowercase snake_case of the given name, dropping apostrophes. Keep stems reasonably short, at most about 40 characters.

### The META block

- `name`: use the given name. You may polish it slightly, but keep it unique.
- `gender`: `"male"` or `"female"` to match your batch.
- `description`: one vivid sentence about what it looks like.
- `tags`: use the existing vocabulary only: `casual work rugged sturdy fancy skirt simple whimsical martial tailored long_skirt robe relaxed holy scholarly slim apron armor sea gown kilt knit`. Don't add `modern` or `denim`, which are reserved for the supreme-casual line.
- Optional keys, as in existing pieces:
  - `"tucked": True` for shirts that go under the waistband.
  - `"covers_waist": True` for a top with its own belt, sash or long hem.
  - `requires`, `rejects` and `locked_to`.
- Lines marked **[locked]** in the plan are designed as one outfit: the top and bottom name each other in `locked_to`. **Every other line must be free** (no `locked_to`) and should mix well with other bottoms.
- Armor pieces: a top tagged `armor` normally `requires: ["sturdy"]` legwear. Plated legs normally `requires: ["martial", "rugged"]`.

### Seeds

Use texture seeds from your batch's seed range (given in the batch's concept section above), so no two pieces share noise.

### Style rules (non-negotiable)

- Casual medieval or fantasy-medieval village wear. **No modern cuts**: no hoodies, zips, logos, prints of text, sneakers, jeans or t-shirts. Regional pieces from the wider medieval world must be respectful and grounded, never costume parody.
- Every piece must be **visually distinct** from every existing piece and from the others in your batch. Give each one a recognisable silhouette or signature detail, such as a 3D cuboid prop or panel, a distinct cut, trim, closure or pattern. A recolor or rename of an existing module is a failure.
- Use the shared helpers, but put each piece's identity in its own module.
- Pixel art should look calm and structured: weave, twill, knit, quilting, hems, seams, buttons, lacing, folds. Avoid random noise.
- Use palette roles sensibly:
  - P is the main cloth.
  - S is the secondary cloth (shirts, linings).
  - A is accent trim.
  - L is leather, M metal, K ink or very dark.
  - Don't use D (denim) or H (hair).
- Work garb should show its trade through props on 3D pieces: tools, pouches, aprons, bundles, baskets, rolls, rope, keys and so on. They must still read cleanly at Minecraft scale.
- **Layering depths:**
  - Top hems and flaps sit at z -2.85 (front) and 1.85 (back).
  - Skirt and kilt panels from bottoms sit at -2.95 / 1.95.
  - Over-layers that must lie over a skirt (aprons, tabards, overdress panels) sit at -3.15 / 2.15.
  - Use `flap_front`/`flap_back` motion on anything below the waist that hangs off the torso, so strides don't clip.
- Props on the back, such as a lute, banner, bundle or coracle, must not intersect the head or arms in walk previews.
- Women's bottoms should be a varied mix: skirts of many cuts and lengths, and also breeches or trews where the concept says so. Footwear goes on the bottoms, as in existing modules.

## Rules for shared files

- **Do not edit any shared file**: `kit*.py`, `paint.py`, `anime*.py`, `wardrobe.py`, `preview.py`, `palettes.json`, `hair_colors.json`, `outfits/male.json`, `outfits/female.json`, docs or Java.
- If you want helpers shared across your batch, create **one** new module, `tools/wardrobe/kit_<batch>.py` (for example `kit_m03.py`), and import it from your pieces.

## Outfit templates

Create **one new file**, `tools/wardrobe/outfits/<gender>_<batch>.json` (for example `male_m03.json` or `female_f07.json`), using the same shape as `outfits/male.json`:

```json
{
  "outfits": [
    {"id": "m_reaper", "name": "Reaper", "top": "t121_...", "bottom": "b121_..."}
  ],
  "professions": {"FARMER": ["m_reaper", ...], "NONE": [...]}
}
```

- **Ids:**
  - One template per line of your batch, pairing that line's top and bottom.
  - Ids are `m_<snake>` for men and `f_<snake>` for women.
  - An id must not collide with any existing id in `tools/wardrobe/outfits/*.json`; grep before you choose.
  - Make ids specific, for example `m_ferry_boatman` rather than `m_ferryman` if similar words exist.
- `name`: a short role name, for example "Reaper" or "Wool Merchant".
- **Professions:**
  - Add each template id to the profession lists given in the plan line.
  - Profession keys: `NONE` (unemployed), `NITWIT`, `ARMORER`, `BUTCHER`, `CARTOGRAPHER`, `CLERIC`, `FARMER`, `FISHERMAN`, `FLETCHER`, `LEATHERWORKER`, `LIBRARIAN`, `MASON`, `SHEPHERD`, `TOOLSMITH`, `WEAPONSMITH`, `KNIGHT`, `ARCHER`, `COOK`, `TAVERN_KEEPER`, `APOTHECARY`, `PAINTER`, `BARD`, `TAILOR`, `CARPENTER`, `SCHOLAR`, plus the archetypes `MERCHANT`, `ADVENTURER`, `GUARD` and `MAGE`.
  - Every template needs at least one non-archetype profession. If a plan line lists only archetypes, add a fitting real job.

## Save progress as you go

- **Commit after every 5 finished outfits.** Each commit holds those pieces plus their entries in your outfit JSON, for example `Add men's tops and bottoms t121-t125 (field and orchard)`. Then if your run is interrupted, the work survives.
- **At the start, check for earlier work.** Run `git log --oneline main..HEAD` and `git status` in your worktree. If an earlier attempt already committed or left pieces, review them briefly and continue from where it stopped. Don't redo finished work.
- **Keep your study phase efficient.** Read the required docs and kits, plus a handful of modules. Don't read dozens of files before writing your first piece.

## Workflow

1. **Compile and validate one piece:**
   ```
   python tools/wardrobe/wardrobe.py --only t121 b121
   ```
   Fix every error: unpainted texels, out-of-bounds pixels, bad bones or atlas overflow.
2. **Preview your work in groups of about 5 outfits:**
   ```
   python tools/wardrobe/preview.py outfits --only t12 b12 --ids m_reaper m_haymaker ...
   ```
   - Add `--back` for the back view and `--walk` for mid-stride.
   - Use `preview.py one --top <id> --bottom <id> [--back] [--walk]` for a single piece.
   - `preview.py tops|bottoms --ids <prefixes>` shows the bare pieces.
   - Previews go to `build/wardrobe-preview/`.
3. **Look at every preview image**: front, back and walk. Fix clipping, unreadable mush, floating props, holes and anything that doesn't read as the concept. Iterate until each piece looks deliberate and good. Quality matters more than speed, but finish all 25.
4. **Run the full compile once at the end:**
   ```
   python tools/wardrobe/wardrobe.py
   ```
   It must print "Compiled N wardrobe pieces" with no errors. That validates catalog rules: templates, professions and the at-least-7-partners mixing rule.
5. **Commit only your sources, in commits of 5 outfits as above, then a final one if needed:**
   - `git add tools/wardrobe/tops/<your files> tools/wardrobe/bottoms/<your files> tools/wardrobe/outfits/<your json> [tools/wardrobe/kit_<batch>.py]`
   - **Do not commit** anything under `src/` or `build/`. Assets are compiled once, when the batch is merged.
   - Commit message, for example: `Add men's tops and bottoms t121-t145 (field and orchard)`.
   - Use the repo's configured git identity and a plain message with no trailers.
