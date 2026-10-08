# Village Friends 2.16.0 — 171 new outfits

- Add 99 men's outfits (each a top and a bottom), 219 tops and 219 bottoms in all:
  - **Field and orchard:** reapers, haymakers, threshers, vine dressers, hedge layers, mole catchers, cowherds, cider pressers, seed sowers, gleaners and dairymen.
  - **River and sea:** ferrymen, bargemen, sailors, shipwrights, caulkers, oyster dredgers, salt boilers, a harbour master, a beacon keeper, a pilot, a sea captain, eel trappers, mudlarks, lock keepers, a coracle man and cockle rakers.
  - **Soldiers and the watch:** pikemen, crossbowmen, halberdiers, hobelars, a sergeant-at-arms, a standard bearer, a war drummer, a castellan, a gate warden, an outrider, a plate-armored lancer, sappers and a siege engineer.
  - **Clergy, learning and healing:** a physician, a barber-surgeon, a chantry priest, a deacon, a cantor, a hospitaller, an almoner, a pardoner, novices and lay brothers, a geometer, a notary, a schoolmaster, an interpreter and a herbalist monk.
  - **Road, forest and mountain:** tinkers, carriers, a royal courier, foresters, a verderer, a gamekeeper, poachers, outlaws, a mountain guide, miners and quarrymen.
  - **The wider medieval world:** Byzantine, Andalusian, Persian, Polish, Hungarian, Basque, Welsh, Breton, Sicilian, Venetian, Alpine, Bohemian, Novgorod and Song Chinese dress.
  - **Everyday village basics:** sixteen plain, mixable shirts, tunics, coats, vests, jackets and trousers for everyday wear.
- Add 72 women's outfits, 132 tops and 132 bottoms in all:
  - **Farm and dairy:** goose girls, haymakers, gleaners, sheaf binders, vintners, dairymaids, egg wives, poultry girls, flax pullers, wool carders, cowherds and orchard girls.
  - **Coast and market:** net menders, oyster sellers, cockle gatherers, ferrywomen, sailors, harbour traders, salt girls, seaweed gatherers and market stallholders.
  - **Warriors and hunters:** crossbowwomen, spearmaidens, a lady sergeant, horse archers, scouts, trackers, militia, a watchwoman, a gate warden and a lancer.
  - **Healers, faith and learning:** a physician, a wise woman, an anchoress, beguines, a canoness, novices, a prioress, lay sisters, an almoner, a governess, an astrolabe reader, an alchemist, an illuminator, a scribe and a seer.
  - **Road and wilderness:** pedlars, tinkers, wanderers, foragers, mushroom gatherers, wood gatherers, charcoal burners, miners, prospectors and mountain herders.
  - **Everyday village basics:** fifteen plain, mixable kirtles, bodices, blouses, jackets and skirts.
- Add six locked one-piece sets (chantry priest, deacon, herbalist monk, Song scholar, anchoress and prioress); everything else mixes freely. 37,077 men's and 14,449 women's free top-and-bottom pairs are allowed.
- Give every new outfit its professions, so new villages dress the new trades. Each batch has its own template file in `tools/wardrobe/outfits/`.
- Save seven planned but unbuilt batches (craft guilds, nobles and the court, and festivals for men; crafts, the court, the wider world and festivals for women) in `tools/wardrobe/backlog/` with their reserved numbers, concepts and helper kits.

# Village Friends 2.15.0 — Village Life grows to 349 clips

- Add 250 clips to the Village Life animation pack (99 → 349 clips, 340 distinct motions), all chosen by the existing director with no new triggers:
  - **Work (75):** three new motions for every vanilla and Village Friends profession, the unemployed and nitwits, such as a smith quenching a blade, a farmer broadcasting seed, a fisherman mending a net, a cleric swinging a censer, a librarian shelving a book up high, a cook tasting the stew, a bard strumming a lute and a scholar's eureka.
  - **Hobbies (24):** two more pastimes for each personality, from knitting and juggling to splitting firewood, sipping tea, tinkering with a gadget and petting a cat.
  - **Everyday moments (30):** cracking knuckles, swatting a bee, hiccups, touching toes, catching a falling leaf, balancing on one leg and more.
  - **Weather and time of day (14):** sheltering from rain, splashing puddles, jumping at thunder, stamping feet in the cold, rubbing sleepy eyes at dawn, nodding off at night, wishing on a star and watching fireflies.
  - **Greetings and conversation (48):** 14 greetings (a curtsy, a hat tip, a fist-to-chest salute, children who jump and wave), 14 talking gestures, and 20 ways for neighbors to speak and listen.
  - **Reactions (43):** six to eight reactions for every conversation outcome and vanilla event, plus three new ways to get hurt.
  - **Children (16):** skipping rope, hopscotch, hobby horses, sandcastles, hide-and-seek, tantrums and marching like a soldier.
- Keep trades and hobbies visible among the new everyday idles: a resident now spends roughly 10–25% of their idle time on work and about a tenth on hobbies.
- Add `tools/animations/vlcheck.py` to check and preview one authoring module on its own, and point the offline previewer at the merged outfit templates.
- Raise `AnimationPackTest`'s coverage bars (four work motions per profession, three hobbies per personality, six or more of each reaction) and lay the `-PanimationPack` gallery out 20 residents wide.

# Village Friends 2.14.0 — Village days, working workstations and 5,898 pieces of dialogue

- Give every resident a daily routine: their own hours (early birds, regular hours, night owls, varying by a few minutes each), breakfast and supper at home, work, a lunch hour at the bell, at home or at the tavern, their hobby at a spot that suits it (water for anglers, flowers for gardeners, a bench for carvers), catching up with the neighbors at the bell, evenings at home or at the tavern, and bed. Jobs keep their own hours: early farmers, fishermen and cooks, clerics' morning prayers, a tavern keeper who works the evening, a bard who performs at the tavern, nitwits who nap after lunch, and about half of all knights and archers on the night watch. Children have lessons by the bell. Every seventh day is Market Day.
- Make the weather matter: rain sends most residents home or under a roof (rain lovers stay out; farmers, shepherds, fishermen, masons and guards keep working), thunderstorms send everyone in except guards on duty, snow keeps the cold-averse by the fire while children play in it, and residents come out with a sparkle when the rain stops.
- Routines drive vanilla's own activities (work, the bell, home, bed, play), so pathfinding, doors, beds, panic, raids and the bell keep working; residents home for breakfast, supper or out of the rain stay awake. The conversation status line shows what a resident is doing and the time, the Village Ledger shows their hours and their day, and animation clips follow it: trade motions during work, hobbies during free time.
- Redesign all eleven Village Friends workstations as detailed multi-part models with new pixel art, and make each one do something. The training dummy measures your hits and combos; the archery target scores arrows 1–10; the kitchen stove cooks raw food twice as fast as a campfire and, once the cook has worked, serves a dish of the day; the drinks barrel presses apples into the new **Mug of Cider** and the tap stand brews coffee; the alchemical press makes Herbal Tonics; the easel paints seven pictures you can take home; the music stand plays ten songs and gives Haste; the sewing table mends leather, bows, rods and elytra with string; the sawmill saws logs into half again as many planks; the archives copy out the village chronicle.
- Residents work at their stations: knights and archers train (archers shoot practice arrows) and gain guard experience, the cook lights the stove, the tavern keeper restocks, the apothecary heals anyone hurt nearby, the painter paints, the bard performs, the tailor mends the guards' armor, the carpenter leaves offcuts and you can study with the scholar for experience. Each custom profession has its own work sound.
- Replace the handful of lines each personality had with **5,898 pieces of handwritten dialogue**: 4,861 lines chosen from the time of day, the weather, what the resident is doing, their personality and job, how well they know you, Market Day, the moon, their hometown, what you're holding and how you look, and who's around; plus 121 questions (would-you-rathers, riddles, dilemmas, questions about you) whose answers residents remember and bring up later, and 25 situational offers that do something: patching you up, a meal, waiting out the rain together, torches, cooking or mending what you hold, directions home and more. Children have their own voice throughout.
- Add `tools/workstations/` (designs, art, previews), `tools/dialogue/` (plain-text dialogue and its compiler), `RoutineTest`, `DialogueBankTest`, `TalkTest` and `WorkstationGameTest`. See VILLAGE_DAYS.md.


# Village Friends 2.13.0 — Village life and new faces

- Give every village a census (`villagefriends:societies`): everyone knows everyone, with a relationship meter from -100 to 100 for every pair. Meters grow over the days two residents have known each other toward a target set by their chemistry (a stable spark, shared personality and a personality matrix), rise with days spent near each other and dip after quarrels. Family starts close.
- Settle natural villages with families: newcomers who arrive with family join a nearby household as a married couple, siblings, or parent and child, and take the household's surname while they still have their generated name. Babies born through vanilla breeding record both parents, join their family and take a parent's surname. Relatives never breed with each other, and residents in love breed only with their partner.
- Add slow love: compatible, unrelated single adults fall in love after their pair's own 50 to 1,000 days of knowing each other and only if they like each other enough. Crushes come first; sweethearts marry after 30 to 150 days. About one resident in five never falls in love. Deaths widow partners; zombie conversions are recorded as curable rather than as deaths.
- Record village news (births, romances, weddings, deaths, curses and cures, newcomers, quarrels and friendships), announce big news to players in the village, and let villages catch up on up to 30 days.
- Make residents talk about each other: neighbors, partners, children and rivals in everyday chat; a "Did you hear?" after big news; **Any village news?** (level 3) with secrets for close friends (level 6); and **Anyone special?** heart-to-hearts (level 5). The Journal lists family, partner, closest friend and rival.
- Add ten friendship levels inside the five tiers, each with a name and an unlock, celebrated once when reached; level 9 friends save you a small daily gift.
- Add Tomodachi Life–style speech bubbles: twelve animated emotes (!, ?, hearts, music, anger, sweat, dots, Zz, sparkles, an idea, gloom and a blush) that pop over residents when neighbors chat (matching how they feel about each other), when they greet you, sleep, get hurt, react in conversation, mourn, or have news for you.
- Rebuild the conversation window: the world stays in view; a dialogue box with portrait, a personality-colored name ribbon and status; numbered reply bubbles (keys 1–6); a dock with item icons for tabs, gifts, trading, the ledger and goodbye; a friendship card with ten hearts and the next goal; a level-up banner; and the resident's mood bubble.
- Add the **Village Ledger** item (book, ink sac, paper) and make Notice Boards open it: every resident with job, family or love life and your friendship level, a page per resident with their story and a meter for every neighbor, and village news.
- Add `tools/social_assets.py` for the bubble sheet and ledger art, `SocietyTest`, `GossipTest`, `FriendshipLevelsTest`, `VillageLifeGameTest` and `-PvillageLifeOnly`. See VILLAGE_LIFE.md.
- Redraw resident faces to look younger and friendlier. Every resident has one of two pixel-art eye styles for life: **Starlit** (a lash line, a tinted white beside a dark pupil, then a glint beside the iris) or **Soft Glint** (a lash line over a glint and the iris).
- Make men's and women's faces distinct: men get straight, fuller brows and a small neutral mouth; women get a lash wing, finer arched brows, rosy lips and blush. Non-binary residents get one or the other.
- Remove the details that aged faces: the eye-bag and chin shadows, the off-center nose, the wide flat mouth and the tiny iris with white showing around it.
- Blink by sweeping the lash line down over the eye; glances slide the iris within the eye. Eyes keep each complexion's original colors.

# Village Friends 2.12.0 — Village Life animation pack and wordless voices

- Replace villager ambient, yes, no, trade, hurt, death and celebrate sounds with synthesised wordless, human-like hums (a `sounds.json` override; generated by `tools/make_voice_sounds.py`).
- Type conversation dialogue out with a pop and soft blips; Space finishes the line. Residents gesture while their line types out, then listen while you choose a reply.

- Add resident animation packs: client resources under `assets/<namespace>/resident_animations/` that resource packs can extend, replace or trim. Clips key rotations and offsets for the head, body, arms, legs, a hip-pivoting waist and a feet-pivoting root, plus eyelids and gaze, sampled with smooth, overshoot-free curves.
- Ship the first pack, Village Life: 99 clips (90 motions) covering everyday idles, a hobby for each of the twelve personalities, a work motion for every vanilla and Village Friends profession, greetings, conversation gestures, neighbor chats, reactions, weather and children's play.
- Give each resident a client-side director: idles paced by personality, neighbors who take turns speaking and listening, greetings when a player walks up, gestures while the conversation window is open, laughs at jokes, cheers or thanks for gifts, polite refusals for disliked gifts and refused trades, and reactions to hearts, angry clouds, happy sparkles, raid sweat and harm. One resident in nine is left-handed.
- Add always-on idle life: a slow weight shift, a drifting gaze between AI look targets, visible breathing in the shoulders, and a forward lean when hurrying.
- Sync each resident's personality to clients (`villagefriends:temperament`) so body language matches the Journal. Turn the head toward the player while greeting or talking.
- Add `tools/animations/` (authoring kit, compiler with `--check`, offline previews and a film assembler), `-PanimationPack` in-game checks with a still of every clip, and a development `-PanimationVideo` showcase.

# Village Friends 2.11.0 — Men's and women's wardrobes

- Split the wardrobe into men's and women's sets. Residents wear their own set's hair, tops, bottoms and profession outfits; non-binary residents wear both. The original 90 pieces become the men's set.
- Add the first women's wardrobe: 50 hairstyles and 60 tops and bottoms, with kirtles, bodices, chemises, overgowns, aprons, skirts, breeches and armor. Every profession has women's outfits and its own preferred look.
- Add 50 men's hairstyles and 70 casual-medieval men's tops and bottoms for trades, clergy, nobles, soldiers, regions and festivals.
- Add a men's *supreme casual* line of 20 tops and 20 bottoms:
  - plain tees and tunics in five colors each;
  - polos, camp-collar, oxford, henley, ringer, raglan, pocket and V-neck tees and a denim work shirt;
  - five jeans and two baggy jeans;
  - chinos, slacks, cargo, carpenter and work pants, cords, linen pants and joggers.
- Add locked sets: a top and bottom that name each other are always worn together and never mixed. There are 19 men's sets and 8 women's sets, such as habits, gowns, the jester's motley and the green man. Everything else still mixes freely, with at least seven partners per top.
- Add a denim material role to every palette, so jeans read as denim while matching the outfit.
- Move outfit templates into one file per set under `tools/wardrobe/outfits/`. Every top must be in a template, and every profession must dress each set.
- Preferred profession outfits now appear 30% of the time and template bottoms 50%, so villages show more of the wardrobe.
- Scale the wardrobe tests and galleries to the gendered sets. Add `-PresidentSample`, which dresses five random men and five random women in Minecraft and screenshots them.

# Village Friends 2.10.1 — Guard spawn eggs

- Add Knight and Archer Spawn Eggs to Creative's Spawn Eggs tab and `/give`, using the existing villager entity rather than separate mobs.
- Spawn equipped adult guards at generated levels 15–30, retaining their profession without a nearby workstation. Support native item accounting and dispensers.
- Verify spawning, equipment, progression and profession persistence through native gameplay fixtures and save/reload.

# Village Friends 2.10.0 — Guard progression

- Give generated and migrated Knights/Archers saved levels 15–30, weighted toward the middle; ordinary residents acquiring either profession start at 0.
- Cap progression at 50, with +0.2 maximum HP and +0.5% direct damage per level. Preserve native weapon/enchantment/protection behavior and arrows' firing-time level.
- Share guard XP on qualifying mob deaths by actual recent health damage, including player/other damage in the denominator. Keep fractional credit and normal Minecraft XP drops.
- Lock the full registered profession on the guard's first qualifying killing blow. Keep combat progression separate from trading XP and friendship, and preserve it through conversion/cure and reload.
- Show level, XP, stat bonuses and combat-lock status in the existing conversation and Journal. Leveling never heals, revives or regenerates equipment.
- Extend `guardsOnly` with native progression and persistence fixtures and add focused balance/contribution policy tests.

# Village Friends 2.9.0 — Knight and Archer defense

- Adult Knights and Archers defend villagers against their predators and actual attackers; Creepers are excluded.
- Unforgiven player damage alerts nearby guards, using the victim's effective friendship before trust penalties. Pursuit and per-player anger are bounded.
- Guards receive persistent mixed iron/chainmail equipment, use native melee and safe bow projectiles, and accept physical equipment exchanges from peaceful players.
- Recruited guards retain follow/wait, owner-only equipment exchanges and downed recovery. Archers have unlimited, uncollectable ordinary arrows.
- Preserve the 2.8 wardrobe and procedural villages. Add focused guard and companion gameplay selectors.

# Village Friends 2.8.0 — Casual medieval and anime hair expansion

- Add twenty casual-medieval tops: belted linen tunic, drawstring smock, clasped half-cloak, quilted arming jacket, laced leather jerkin, liripipe hood, fur-trimmed houppelande, buttoned cotehardie, sheepskin vest, wrapped wool shawl, herbalist's bandolier, tavern shirt and half-apron, fur-collared coat, hooded wool poncho, layered overtunic, embroidered festival vest, woodsman's wrap jacket, baker's floury smock, satchel and overshirt, and student's open gown.
- Add twenty casual-medieval bottoms: cross-gartered hose, knee braies, tartan trews, buttoned gaiters, belted wool kilt, sheepskin leg wraps, side-laced leather trousers, wool trousers with clogs, striped stockings, drawstring trousers, fur-topped boots, tall riding boots, pouch-belt trousers, woolen chausses, summer sandals, quilted trousers, knee breeches, leather chaps, belted hose with dagger, and embroidered hem trousers.
- Add twenty anime-inspired hairstyles with cel-shaded clumps, a sheen ring and pointed tapered locks: pointed bangs, hime cut, long sidelocks, wolf cut, ahoge bob, side-swept bangs, high ponytail, back braid, pointed layers, swept-back spikes, half-up bun, long curtains, undercut curtains, sleepy fluff, long low tail, headband spikes, wavy layers, braided crown, ronin tail and rat-tail crop.
- Add twenty outfit templates and give each profession a short list of fitting outfits; the preferred template is chosen 60% of the time. Kilts and sandals reject armor; 861 of 900 top/bottom pairs mix.
- Give the resident atlas one shared slot per garment kind (256×512), so the wardrobe can grow without growing the texture, and only touch the worn garments' parts each frame.
- Add `kit.py` and `anime.py` building blocks, `tops`/`bottoms` preview modes and `--ids` filtering. The compiler now rejects negative inflation and templates no profession wears.
- Page the gametest galleries ten per page, with an in-world scene per page.

# Village Friends 2.7.0 — Sims-style wardrobe

- Replace the outfit engine and every old garment and hair model with a palette-locked pixel-art wardrobe of ten hairstyles, ten tops and ten bottoms.
- Paint garments as key colors (role + shade) resolved through five-shade, hue-shifted ramps of the ten master palettes; one palette per outfit, natural hair colors separate.
- Use the player overlay layers for depth, plus textured 3D pieces: pauldrons, collars, mantles, coat skirts, hoods, quivers, pouches, cuffs, buns, ponytails and layered hair locks.
- Let coat skirts, aprons and tabards follow the leading leg; let ponytails, tassels and sash tails sway.
- Mix any top with any compatible bottom; tag rules keep armor with sturdy legwear and hose away from armor and aprons.
- Map professions to ten outfit templates; keep hair and hair color when a resident changes jobs.
- Add `tools/wardrobe/` (one module per piece, compiler, offline previews) and gametest galleries of all outfits, hairstyles, mixes, palettes and an in-world scene.

# Procedural plains villages

- Replace the fixed 13-piece plus-shaped village with procedural jigsaw villages: three town centres, terrain-following streets with bends, turns, junctions and well squares, and street ends with fading paths, lamps or a timber gatehouse.
- Ring every square with the guaranteed civic buildings (tavern, garrison and watchtower, workshop, chapel and graveyard, apothecary, library); all ten new professions appear in every village.
- Add timber-framed cottages, two-storey and jettied houses, townhouses, a farmhouse, vanilla trade workshops, fields, paddocks with livestock, apiaries and street-side details. Chimneys smoke; roads become plank bridges over water; stone weathers with moss.
- Author buildings as Python design programs (`tools/village_design/`) that compile to independent blueprints, with automatic fence/pane/wall/stair states, door-clearance and bedroom checks, hand-edit protection, a layout simulator and an in-game screenshot gallery.
- Generalise the lot contract (any size up to 32, entrance at `[x,1,0]`), add layout format 2 (fallbacks, empty entries, projections, processor lists) and make the structure test accept procedural assemblies.
# Male starter set and texture overhaul

- Replace the 150 male entries with five hairs, five tops and five bottoms.
- Replace stretched solid texels with multi-texel cuboid face UVs, deterministic HSV woven/leather/hair grain and geometry-derived overlap shadows.
- Remove floating knee/shin patches and duplicate belts; keep connected collars, cuffs, coat hems and one waist belt.
- Add stepped crowns, fringe/side overhangs, forehead shadows, trouser seam shading and connected leather boots.
- Bake outfit-specific 512×512 atlases; use version 4 recipes and regenerate older male appearances through the starter set.
- Hold female expansion outside the active catalog; capture five revised male outfits inside Minecraft.
# Male asset registry — Phase 2

- Add all 150 explicit male IDs: 50 hair models, 50 tops and 50 bottoms, grouped in compact JSON arrays.
- Compile exact disjoint four-role material bounds with 60/30/10 textile pixel coverage and separate hardware coverage.
- Build distinct solid geometry, use the registries in male outfit assembly, and share identical material swatches.
- Introduce version 2 recipes while preserving Phase 1 selections; add registry and native renderer checks.
# Outfit engine rebuild

- Remove the previous wardrobe code, preset resources, generators and obsolete wardrobe tests.
- Add ten master palettes, four-channel role masks, validated hair/top/bottom models and a palette-locked outfit factory.
- Render the new solid voxel silhouettes on animated resident bones; reset retired appearance recipes while preserving resident history.
- Add core invariants and focused Minecraft renderer verification. Earlier entries below describe retired releases.
# 2.6.0

- Give residents six stable, understated gaits with individual cadence, stride, shoulder swing, balance and step height. Children take lighter, quicker steps.
- Add quiet breathing, small head tilts, softly moving braids, satchels and scarf tails.
- Add articulated eyes using the original complexion and eye colors, with varied blink timing, occasional double blinks, subtle idle glances and nearby eye contact. Hair and glasses stay in front of the eyes.
- Animate armor with the same poses. Preserve sleeping, seated, airborne, swimming, crouching, item-use and attack behavior; sleeping eyes close.
- Preserve saved recipes, identities, names, relationships and every skin asset. No per-frame textures or new saved animation records.
- Add native Minecraft art previews and animation/compatibility/navigation/reload checks.

# 2.5.0

- Complete Codex Phase 3 with 494 separately editable JSON definitions and 366 native 64×64 material masks for the local compositor.
- Independently combine 96 tops, 64 bottoms, 72 hairstyle variants, 96 clothing palettes, 32 hair colors and 32 clothing details using stable saved `m3` recipes.
- Add straight, slim, relaxed, bootcut and ripped jeans, each in eight casual washes, plus six other trouser families.
- Add partial work layers for all 23 professions, preserving personal trousers, uncovered shirts, faces and hair.
- Import and deduplicate the supplied name list, retaining existing names: 1,097 first names and 250 surnames. Restrict the supplied Indian pool and overlapping surname to brown/dark complexion indices 2–5.
- Generate names after assigning the actual saved complexion. Preserve existing/custom names, earlier recipes, child identity, growth and save/reload.
- Document individual layer edits, semantic masks, palettes, data/resource packs and the developer handoff. Add focused and full Minecraft verification.

# 2.4.0

- Implement Phase 2 with fifteen native structure templates, thirteen jigsaw pools and a complete connected village layout: plaza, tavern, garrison, cemetery, enclosed homes, apothecary, workshop and library.
- Add natural plains/meadow generation alongside vanilla villages, with separate placement and vanilla-village exclusion. Integrate the new structure with existing hometown discovery.
- Place fourteen starter residents, all ten new profession anchors, benches, treatment cots, administrative blocks, beds and practical building interiors.
- Provide three cottage variants, separately enclosed bedrooms and clear doors for future spatial bed scans. The scanner and specialized AI remain later work.
- Add deterministic template tooling and Minecraft tests for loading, rotation, room boundaries, assembly, natural generation and persistence.
- Keep every building in a separate editable layered JSON blueprint, with independent role pools, single-building regeneration and a documented handoff and entrance contract.

# 2.3.0

- Implement the master specification's Phase 1 foundation: ten professions and their distinct workstation POIs, preserving vanilla job anchors.
- Add 17 directional blocks, four registered block entity types with public integration hooks, and self-drop loot tables.
- Add 24 items: medical supplies, meals/coffee, weather wearables, ten uniforms and five tools. Meals heal; coffee grants Speed I; wearable equipment renders on players and companions.
- Package original pixel art, block/item/equipment models, localization, 41 crafting recipes/unlocks, and 50 trade sets with 100 offers. Revival Tonic requires an Awkward Potion.
- Add reproducible asset tooling and actual Minecraft verification of natural profession acquisition, crafting, trading, placement, loot, consumption, rendering and save/reload.
- Document the hooks and remaining behavior in PHASE1.md. Specialized AI, real-time revival, seating, housing scans, worldgen and advanced animations remain later work.

# 2.2.0

- Align all glasses around the actual iris pixels; remove duplicated, misaligned painted frames from older hairstyles and the Ink resident at composition time.
- Add five frame styles alongside round glasses: rectangular, octagonal brass, browline, half-rim and aviator, each with its own geometry/material.
- Add specific clothing for all 13 working professions, with consistent occupational colors and eight personal trim variations per job.
- Give garments physical depth with raised panels, collars, articulated sleeves/cuffs, hanging aprons, coat tails, book pockets, a map roll, quiver, smith shoulder plates and belt pouches.
- Update clothes immediately from the synced vanilla profession while retaining saved appearance recipes, faces, names, friendship and trade behavior.
- Keep child play-clothes and hide conflicting garment/eyewear geometry under armor.
- Add geometry/asset checks and an actual Minecraft wardrobe test covering all professions, six frames, old appearances, job changes, portraits, trading and reload.

# 2.1.0

- Give children proportionally larger heads, shorter bodies, child faces and six play-clothes designs in the world and live portrait. Preserve identity when they grow up.
- Discover and save natural village names; add "First Last of Village" hover names, village welcome messages, hometown dialogue and journal entries.
- Add a craftable carved Village Marker for player-built settlements, anvil naming/renaming, right-click information and persistent origins after removal.
- Preserve hometowns through travel, conversion, curing and reload; preserve old names as the personal part and keep existing friendship, trades and adult appearance recipes.
- Add 2,400 personality-directed appearances, six additional hairstyles, eight additional outfits, eight facial details and ten articulated accessories. Retain all 2,000 original recipes.
- Add actual outer garment/hair layers and small 3D hats, glasses, bags, jewelry, scarves and hair shapes; hide accessories that conflict with armor.
- Wrap long hometown names in the conversation card and expose full names and metadata on hover.

# 2.0.0

- Preserve 1.1.0 names, skins, points, daily limits, trades, and unlocked tiers; migrate to stable resident IDs and modular recipes.
- Add persistent personalities, hobbies, values, preferences, private trust, permanent story flags, recent memories, and resident friendships.
- Add eight authored four-chapter stories, 24 requests, twelve dialogue profiles, branching endings, and reciprocal gifts.
- Add Story, Journal, Time, and Travel controls with a live equipment-aware portrait.
- Add walks, picnics, exploration, gatherings, and personal invitations.
- Add one Overworld melee companion per player, equipment exchange, follow/wait/home, downed rescue, home recovery, and owner-state cleanup.
- Preserve identity through conversion and curing; keep shared request credit separate from private relationships.
- Add 2,000 original modular appearances with local composition, texture caching, fallback handling, and reproducible art tooling.
- Gate upper friendship tiers on experiences and stories; retain existing tiers during migration and avoid absence penalties.

Romance/family, dimension travel, ranged roles, and larger parties remain future work.


