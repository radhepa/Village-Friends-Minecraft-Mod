# Village Friends RPG

A separate mod (`villagefriends_rpg`, its own jar) that turns a Village Friends world into a slow-burn RPG.
It **requires Village Friends 2.29.0+** (1.1.0 adds Riding, which listens to Village Friends' Stablehand); Village Friends still works fine without it.
1.2.0 knows the **whole Village Friends modpack** (see [The modpack](#the-modpack)): every other mod is optional, and its monsters, places and jobs only appear when it's installed.

Build: `gradlew :rpg:build` → `rpg/build/libs/villagefriends-rpg-<version>.jar`. Put it in `mods/` next to the Village Friends jar.

## The shape
- **You start at half strength**: 5 hearts, 50% hungrier, and melee damage, projectile damage and block-breaking speed all at **50%** of vanilla.
- **You earn vanilla back by level 30**: a heart every 6 levels, and damage, breaking speed and hunger climb evenly with each level.
- **Then you keep growing to level 100** (~730k XP, roughly 100+ hours): a heart every 14 levels (15 hearts at 100), +0.2% base damage and breaking speed per level (+14% at 100) and 15% less hunger, on top of attributes, skills and masteries. A full-Vitality, fully mastered tank tops out near 25 hearts; a level-100 character is clearly stronger than vanilla, but not a god.

| Level | Hearts (before Vitality/perks) | Damage, breaking speed | Hunger drain |
|---|---|---|---|
| 1 | 5 | 50% | ×1.5 |
| 12 | 7 | 69% | ×1.31 |
| 24 | 9 | 90% | ×1.10 |
| 30 | 10 (vanilla) | 100% | ×1.0 |
| 58 | 12 | 106% | ×0.94 |
| 100 | 15 | 114% | ×0.85 |

- **Keys**: **K** character sheet (Overview, Attributes, Skills, Bestiary, Jobs, Atlas), **R** use your Legend ability, **G** switch ability. A small badge top-left shows level, XP and the ability's cooldown.
- **Bosses stay bosses**: against bosses only half of your damage bonus counts, and that bonus can't exceed 4% of the boss's max health per hit. A maxed character still needs ~17 hits on the Warden and ~8 on the dragon.
- **Death** costs 25% of your progress toward the next level, never a level.

## Character level
XP from kills (by the mob's health and rarity), ore, harvests, fishing, breeding, enchanting, trading and, above all, **villager jobs**.
Each level gives 3 attribute points (5 on every 10th): 317 by level 100. Ten attributes cap at 50 each (500 total), so every character is a build. "Unlearn" on the sheet refunds all points for 5 + level/2 emeralds.

| Attribute | Per point (cap 50) |
|---|---|
| Vitality | +0.2 max health (+5 hearts at 50) |
| Strength | +1% melee damage |
| Dexterity | +0.8% attack speed |
| Agility | +0.2% speed, +0.2% jump, +0.06 safe fall |
| Endurance | −0.8% hunger, +0.04 breath |
| Toughness | +0.12 armor, +0.05 toughness |
| Precision | +0.4% crit chance (+50% damage), +0.6% projectile damage |
| Luck | +0.04 luck, +0.5% chance to roll a mob's loot twice |
| Wisdom | +1% character and skill XP |
| Recovery | heal half a heart every (12 − 0.15×points) s while fed |

### Kill XP fatigue
- Kills of the same kind within 30 s of each other are "in a row": the 1st gives full XP, the 2nd–10th give **50%**, and past 10 it keeps dropping (×0.8 per kill, down to 5%). A 30 s break resets it.
- **Mass kills**: 5+ kills of anything within 4 s give ×0.25, 10+ give ×0.1 (on top of the above). Mob farms, TNT and grinders barely pay.
- The action bar shows the share, e.g. `+6 XP (Zombie, 50%)`.

## Skills (0–50, rise by doing)
Swordsmanship, Axe Mastery, Archery, Defense, Mining, Woodcutting, Excavation, Farming, Fishing, Husbandry, Athletics, Swimming, Acrobatics, Arcana, Bartering, Cooking, Riding (17 in all).
Cooking trains when you take food out of a Hearth & Harvest cooking pot, clay oven or prep table (more for better dishes): +1% Well Fed time and a 0.8% chance of a "fine" dish per level (`Cooking.java`, through `HearthEvents`).
Fishing trains on every fish you land, more for rarer fish and perfect catches in Tall Tales Fishing's minigame: +0.03 luck, a slightly bigger catch zone and +0.6% reel speed per level (`Angler.java`, through `FishingEvents`).

Husbandry trains from breeding, hunting livestock and **taming** any animal (wolves, cats, horses, Not-So-Vanilla Mobs' pets and mounts, End Friends' Driftrays): 15 skill XP and 5 XP a tame.
With Turning Seasons, ripe crops teach **25% more Farming in autumn**.

Riding trains on horseback (a point per 5 blocks ridden, donkeys and mules too), from grooming and feeding your own horse (half a point per bond point earned) and from couched Jousting Lance hits (6 each): per level +0.2% horse speed while you ride, +1% bond growth, +0.4% lance damage and 0.6% steadier mounted aim (`Riding.java`, through Village Friends' `StablehandEvents`; Stablehand applies the bonuses itself).
At 50: +20% sword/axe damage, +30% projectiles, +50% tool speed, 20% double ore, 30% double logs, 50% extra harvest, +1.5 luck, +10% speed, −30% fall damage, +50% vanilla XP, +50% job rewards, and so on (exact numbers on the sheet).

## Bestiary (22 monster families, 25 with the modpack)
Kills climb five tiers: **Novice, Hunter, Slayer, Bane, Legend** (common mobs at 25/100/300/750/1500 kills, uncommon 15/60/180/450/900, rare 5/20/60/150/300, elite 1/3/6/10/15, bosses 1/2/3/5/8).
Every tier: +2% damage to them, −2% damage from them. **Slayer** and **Legend** each unlock an ability, for example:
- Zombies: Strong Stomach (no Hunger) → Grave Resolve (survive a killing blow at 4 HP, every 20 min)
- Skeletons: Bone Archer (+15% projectiles) → Deadeye (+20% more)
- Spiders: Venom Ward (no Poison) → Night Eyes (Night Vision underground)
- Creepers: Blast Hardened → Defuser (−60% explosion damage)
- Endermen: Pearl Thrift (pearls don't hurt) → Steady Gaze (looking doesn't anger them)
- Piglins: Gilded Guile (treated as wearing gold) → Hellbound (+15% in the Nether)
- Illagers: Raid Veteran → Village Hero (permanent Hero of the Village)
- Phantoms: Membrane Harvest → Insomnia Ward (phantoms stop coming)
- …plus Vermin, Slimes, Blazes, Witches, Drowned, Guardians, Wither Skeletons, Ghasts, Shulkers, Breezes, the Warden, the Wither, the Ender Dragon and Elder Guardians.
- **Challengers** (Not-So-Vanilla Mobs' ten mini-bosses, elite): Trophy Hunter (they drop their loot twice) → Giant's Heart (+1 heart)
- **The Plata Clan** (rare): Keen Eye (disguised Plata within 24 blocks shimmer silver, only for you) → Shardproof (−20% projectile damage)
- **The Silver Mother** (boss): Brood Ward (−30% damage from silverfish, endermites and the Clan) → Silver Heart (+2 hearts)

### Legend abilities (R to use, G to switch)
Legend in a family also unlocks an **active ability**. Each has its own cooldown, a hunger cost (you can't use them at 3 hunger bars or less), and a 1 s shared cooldown. They reuse vanilla mechanics, and offensive ones only hit monsters.

| Family | Ability | Cooldown, hunger |
|---|---|---|
| Endermen | Ender Blink: teleport to the block you look at (24 blocks), no pearl | 20 s, 2 |
| Zombies | Undead Vigor: Regeneration II 6 s | 90 s, 3 |
| Skeletons | Hunter's Sight: monsters within 32 blocks glow 10 s | 45 s, 1 |
| Spiders | Web Shot: target gets Slowness IV 4 s | 30 s, 1 |
| Creepers | Controlled Blast: up to 8 damage within 4 blocks, no block damage, costs you 1 heart | 60 s, 2 |
| Vermin | Burrow Rush: Haste II 20 s | 120 s, 2 |
| Slimes | Bounce: spring ~6 blocks up, no fall damage 8 s | 20 s, 1 |
| Blazes | Fire Bolt: blaze fireball | 8 s, 1 |
| Witches | Witch's Draught: heal 2 hearts, clear harmful effects | 120 s, 2 |
| Drowned | Riptide: launch forward, in water or rain | 15 s, 1 |
| Piglins | War Cry: Strength I 10 s | 90 s, 2 |
| Illagers | Evoker Fangs: a line of fangs 11 blocks ahead | 30 s, 2 |
| Guardians | Tidal Sight: Conduit Power 60 s | 180 s, 1 |
| Wither Skeletons | Withering Strike: next melee hit gives Wither II 5 s | 30 s, 1 |
| Ghasts | Ghast Fireball (explodes) | 30 s, 2 |
| Phantoms | Night Glide: Slow Falling 15 s and a push | 45 s, 1 |
| Shulkers | Shulker Bolt: target levitates 4 s | 25 s, 1 |
| Breezes | Wind Burst: blow monsters back, hop up | 15 s, 1 |
| Warden | Sonic Boom: 10 damage through armor, 15 blocks | 60 s, 4 |
| Wither | Wither Skull | 20 s, 2 |
| Ender Dragon | Dragon Roar: 6 damage within 8 blocks, knockback | 90 s, 3 |
| Elder Guardians | Abyssal Ward: Resistance II 8 s | 120 s, 2 |
| Challengers | Second Wind: 4 hearts of Absorption 20 s, Speed I 10 s | 120 s, 3 |
| The Plata Clan | Molt: shed harmful effects, then Invisibility and Speed II 5 s | 60 s, 2 |
| The Silver Mother | Mother's Shriek: monsters within 10 blocks get Weakness II and Slowness 8 s | 60 s, 2 |

## Villager jobs
Talk to a resident and choose **"Any work for me?"** (it appears in Village Friends' own conversation window).
Their trade decides the work: guards, knights and weaponsmiths want monsters slain; smiths and masons want ore and stone; farmers, cooks and butchers want food and breeding; fishermen want fish; librarians and scholars want enchanting and books; cartographers, painters and bards send you to far biomes, the Nether and the End; and so on (23 professions).
Each villager offers one job a day; you can hold 3 (4 at level 30, 5 at level 60). Jobs scale with your level and pay XP, emeralds and Village Friends friendship. Return to the villager to turn it in.
Explorers, cartographers, painters and bards can also send you to **find a place** from the Atlas (a Delvers' Camp, the Pearl Grotto, a Cirri sky village, a Piglin Hold, an Endarch Citadel...): it counts the moment you stand inside one.

## The modpack
The add-on cross-references every other mod of the Village Friends modpack. None is required; each piece switches on when its mod is installed (`Modpack`), and `gradlew :rpg:runServer -Paudit=true -PpackMods=<instance mods folder>` boots a server with the whole pack and checks that every monster, place, item and profession named below really exists (`ModpackAudit`).

| Mod | What the RPG does with it |
|---|---|
| **Not-So-Vanilla Mobs** | Its variants count toward their vanilla kin (Sporeling, Frostbitten, Lost Miner, Scarecrow → Zombies; Briarbones, Gravewarden, Soulpyre, Sculkbones → Skeletons; Dune Scorpion, Dripfang → Spiders; Bog Lurker → Slimes; Gloomwing, Vulture → Phantoms; Angler → Guardians; Driftcap → Endermen). The ten challengers get their own **Challengers** family. Gloomwings and Vultures count as flying for Sky Hunter. Taming its pets and mounts trains Husbandry. Guards may ask you to defeat a Challenger. |
| **The Plata Clan** | Its members are **The Plata Clan** family (Keen Eye sees through their disguises), the **Silver Mother** is a boss family, guards and clerics may ask you to unmask Plata or defeat the Mother, smiths and leatherworkers want Silver Scales, and Scale Dens and Silver Warrens are in the Atlas. The clan already reads your RPG level to size you up. |
| **Cave Expansion** | Its miners give **delver** jobs (ore, stone, raw metals, finding the Buried Seam, the Glimmering, the Ossuary or the Sunken Forge); all eight delves are in the Atlas. |
| **Ocean Expansion** | Lightkeepers give explorer and fishing jobs, smugglers give **smuggler** jobs (gold, pearls, ambergris, spying on Tidewatch Fort or the Sunken Galleon); pearls, black pearls and ambergris turn up in fishermen's, clerics' and scholars' jobs; all ten sites are in the Atlas. |
| **Sea Friends** | Merfolk and Prismari give work by trade: pearl divers, kelp farmers, shellwrights, tide singers, lightwrights and spongekeepers each have their own job list (Tidepearls, Conches, Kelp Wraps, prismarine, guardians); Reef Towns and Prism Courts are in the Atlas. |
| **Sky Friends** | Sky Peaches and Sky Scales show up in cooks', clerics', scholars' and painters' jobs; sky villages, islets, Wind Shrines and ruined belltowers are in the Atlas. |
| **Nether Friends** | Its five village kinds (Hold, Vigil, Mooring, Loom, Eave) are in the Atlas. Piglins recoded around gold use vanilla's gold check, so **Gilded Guile** (Slayer of Piglins) also makes them talk to you. |
| **End Friends** | Shulkin Spires, Chorrin Steads, Crossings and Endarch Citadels are in the Atlas (tier 5). Its peoples are never prey: no XP or masteries for them. |
| **Turning Seasons** | Jobs follow the season: no crop jobs in winter (hay, bone meal, wool and stews instead), seeds and breeding in spring, pumpkins and big harvests in autumn. Autumn's harvest teaches 25% more Farming. |

## The Atlas (K → Atlas)
Every place the installed mods build: Village Friends' villages and homesteads, Plata hideouts, Cave Expansion's delves, Ocean Expansion's sites, Sea Friends' towns, Sky Friends' sky, Nether Friends' villages and End Friends' villages and Citadels (45 places with the full pack). Each shows **???** until you've stood inside one. The first visit is a **discovery**: 10% of your current level's XP for a nearby place, up to 30% for an End Citadel (stars = tier).

## Config and commands
`config/villagefriends_rpg.json`: `xpRate`, `skillXpRate`, `deathPenalty`, `bossBonusShare`, `bossHitCap`, `hardStart`.
`/rpg` prints your character. Operators: `/rpg admin <player> level|xp|skill|kills|reset …` for testing.

## Code map
Pure (unit-tested in `RpgBalanceTest` and `ModpackTest`): `Balance` (every number), `Attr`, `Skill`, `Bestiary`, `QuestBook`, `Sheet`, `Quest`, `Modpack` (which pack mods are installed), `Atlas` (the places).
World: `Rpg` (init, synced player attachment), `Life` (attributes, pulse, Keen Eye, buttons), `Hunt` (damage, kills, blocks, taming), `Abilities` (Legend actives), `Progress` (XP and celebrations), `Quests` (conversation glue), `Discoveries` (Atlas finds), `Seasons` (Turning Seasons by reflection), `ModpackAudit` (the dev audit's name check).
Village Friends is hooked from outside with mixins on `NarrativeEngine.choices` and `VillageFriends.handleAction`; no Village Friends code is changed. `Cooking` and `Riding` listen to Village Friends' public events (`HearthEvents`, `StablehandEvents`); Riding's distance comes from vanilla's horse statistic through `Life`'s tracked stats.
`gradlew :rpg:runServer -Paudit=true` boots a dev server, applies every mixin and stops (a quick wiring check); add `-PpackMods=<folder> -PserverHeap=2g` to boot it inside the whole modpack.
Taming is caught with one mixin on vanilla's `TameAnimalTrigger`, which modded pets fire too.

## Versions
- **1.2.0**: knows the whole modpack (families, jobs, Atlas, seasons, taming); harder start (50%, 5 hearts) earned back by level 30, slow growth to 100.
- **1.1.0**: Riding (Stablehand), Cooking (Hearth & Harvest), Fishing tuning (Tall Tales Fishing).
- **1.0.0**: levels, attributes, skills, Bestiary, Legend abilities, villager jobs.
