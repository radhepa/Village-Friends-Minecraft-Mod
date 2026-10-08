# Village Friends RPG

A separate mod (`villagefriends_rpg`, its own jar) that turns a Village Friends world into a slow-burn RPG.
It **requires Village Friends 2.23.0+**; Village Friends still works fine without it.

Build: `gradlew :rpg:build` → `rpg/build/libs/villagefriends-rpg-<version>.jar`. Put it in `mods/` next to the Village Friends jar.

## The shape
- **You start weak**: 6 hearts, 40% hungrier, swings at 85% and mining at 80% of vanilla.
- **Vanilla by level 15–20**, then you keep growing to **level 100** (~730k XP, roughly 100+ hours).
- **Press K** for the character sheet (Overview, Attributes, Skills, Bestiary, Jobs). A small level badge sits top-left.
- **Bosses stay bosses**: against bosses only half of your damage bonus counts, and that bonus can't exceed 4% of the boss's max health per hit. A maxed character still needs ~17 hits on the Warden and ~8 on the dragon.
- **Death** costs 25% of your progress toward the next level, never a level.

## Character level
XP from kills (by the mob's health and rarity; repeated kills of one kind in a short time are worth less, down to 20%, so mob farms don't trivialise it), ore, harvests, fishing, breeding, enchanting, trading and, above all, **villager jobs**.
Each level gives 3 attribute points (5 on every 10th): 317 by level 100. Ten attributes cap at 50 each (500 total), so every character is a build. "Unlearn" on the sheet refunds all points for 5 + level/2 emeralds.

| Attribute | Per point (cap 50) |
|---|---|
| Vitality | +0.3 max health |
| Strength | +1% melee damage |
| Dexterity | +0.8% attack speed |
| Agility | +0.2% speed, +0.2% jump, +0.06 safe fall |
| Endurance | −0.8% hunger, +0.04 breath |
| Toughness | +0.12 armor, +0.05 toughness |
| Precision | +0.4% crit chance (+50% damage), +0.6% projectile damage |
| Luck | +0.04 luck, +0.5% chance to roll a mob's loot twice |
| Wisdom | +1% character and skill XP |
| Recovery | heal half a heart every (12 − 0.15×points) s while fed |

## Skills (0–50, rise by doing)
Swordsmanship, Axe Mastery, Archery, Defense, Mining, Woodcutting, Excavation, Farming, Fishing, Husbandry, Athletics, Swimming, Acrobatics, Arcana, Bartering.
At 50: +20% sword/axe damage, +30% projectiles, +50% tool speed, 20% double ore, 30% double logs, 50% extra harvest, +1.5 luck, +10% speed, −30% fall damage, +50% vanilla XP, +50% job rewards, and so on (exact numbers on the sheet).

## Bestiary (22 monster families)
Kills climb five tiers: **Novice, Hunter, Slayer, Bane, Legend** (common mobs at 25/100/300/750/1500 kills, uncommon 15/60/180/450/900, rare 5/20/60/150/300, bosses 1/2/3/5/8).
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

## Villager jobs
Talk to a resident and choose **"Any work for me?"** (it appears in Village Friends' own conversation window).
Their trade decides the work: guards, knights and weaponsmiths want monsters slain; smiths and masons want ore and stone; farmers, cooks and butchers want food and breeding; fishermen want fish; librarians and scholars want enchanting and books; cartographers, painters and bards send you to far biomes, the Nether and the End; and so on (23 professions).
Each villager offers one job a day; you can hold 3 (4 at level 30, 5 at level 60). Jobs scale with your level and pay XP, emeralds and Village Friends friendship. Return to the villager to turn it in.

## Config and commands
`config/villagefriends_rpg.json`: `xpRate`, `skillXpRate`, `deathPenalty`, `bossBonusShare`, `bossHitCap`, `hardStart`.
`/rpg` prints your character. Operators: `/rpg admin <player> level|xp|skill|kills|reset …` for testing.

## Code map
Pure (unit-tested in `RpgBalanceTest`): `Balance` (every number), `Attr`, `Skill`, `Bestiary`, `QuestBook`, `Sheet`, `Quest`.
World: `Rpg` (init, synced player attachment), `Life` (attributes, pulse, buttons), `Hunt` (damage, kills, blocks), `Progress` (XP and celebrations), `Quests` (conversation glue).
Village Friends is hooked from outside with mixins on `NarrativeEngine.choices` and `VillageFriends.handleAction`; no Village Friends code is changed.
`gradlew :rpg:runServer -Paudit=true` boots a dev server, applies every mixin and stops (a quick wiring check).
