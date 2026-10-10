# Stablehand: horses worth caring about

Version 2.29 adds Stablehand. Every horse now belongs to one of eight medieval breeds with its own stats and painted coat; the horse you ride, feed and brush grows a bond with you that makes it a little faster, steadier and finally comes when you whistle; new tack and four barding tiers render on the horse; villages build stables with a stablehand who sells horses and gear; a couched lance rewards a real gallop; knights ride their night patrols; and taking a village's horse is a deed residents remember. There is no new horse entity: breeds and bonds are saved data on vanilla horses, donkeys and mules.

## Breeds

Every horse gets a breed the first time it loads, picked by the biome it stands in. Foals take one parent's breed (half the time each, when the parents differ) and a blend of both parents' stats, a little wider than either, so good parents tend to give good foals. Brush a horse you own with the Grooming Brush to see its breed, bond and stats on the action bar.

| Breed | Health | Top speed | Jump | Found in | Village stables |
|---|---|---|---|---|---|
| **Destrier** (the war horse) | 26–34 | 8.4–11.0 blocks/s | 1.9–3.3 blocks | plains (rare) | plains |
| **Palfrey** (the smooth riding horse) | 20–26 | 10.1–12.6 | 2.2–3.6 | plains, meadows, forests | plains |
| **Courser** (the racer) | 16–22 | 12.2–14.2 | 2.9–4.9 | plains, savanna | plains, savanna |
| **Rouncey** (the everyday horse) | 18–26 | 8.4–11.4 | 1.9–3.6 | anywhere (the fallback) | plains, taiga |
| **Draft Horse** | 28–36 | 6.3–8.4 | 1.1–1.9 | plains, forests, taiga (rare) | plains, taiga, snowy |
| **Desert Horse** | 16–22 | 11.8–14.3 | 2.5–4.4 | desert, badlands | desert |
| **Steppe Pony** | 20–26 | 9.3–11.8 | 3.3–5.3 | savanna, windswept hills | savanna |
| **Fjord Horse** | 22–28 | 7.6–10.1 | 2.2–3.6 | taiga, snowy plains | taiga, snowy |

Vanilla wild horses range over 15–30 health, 4.7–14.2 blocks/s and 1.1–5.3 blocks. Six breeds have two painted coats and the steppe pony and fjord one; vanilla's white socks, blazes and spots still draw on top. Foals have their own painted coats.

**Horses where vanilla has none.** Fjord horses and steppe ponies also spawn in taiga, snowy and windswept biomes. Vanilla only lets horses spawn on grass, so desert and badlands horses arrive as **sand herds** (two or three horses) placed when a desert or badlands chunk is first generated (about one new desert chunk in 60 and one badlands chunk in 120), never more than 32 chunks a tick and only while the `spawn_mobs` game rule is on.

## Bond

Riding, feeding and grooming a horse you own grows your bond with it, from 0 to 1000 points across five tiers. Only the horse's owner bonds with it; a horse that changes hands starts again from Wary with its new owner.

| Tier | Points | What it adds |
|---|---|---|
| Wary | 0–99 | nothing yet |
| Familiar | 100–249 | +1.5% speed, +1.25% jump, +1 health |
| Trusting | 250–499 | +3% speed, +2.5% jump, +2 health |
| Loyal | 500–799 | +4.5% speed, +3.75% jump, +3 health; **the Horse Whistle calls it** |
| Devoted | 800–1000 | +6% speed, +5% jump, +4 health |

Each tier also makes the horse calmer near monsters (see **Not-So-Vanilla Mobs** below) and adds 2.5% to couched lance damage. Hearts, a neigh and a line on the action bar mark each new tier.

Care is capped each day, so a bond takes days rather than one long session:
- **Grooming** with the **Grooming Brush** (wheat, string and a stick, corner to corner; 128 strokes): 20 points for the first stroke of the day, 2 for the next two. Every stroke heals the horse a little; on an untamed horse the brush calms its temper, which makes taming easier.
- **Feeding**: 5 points for ordinary horse food (wheat, sugar, apples, carrots, hay bales), 15 for a golden carrot or golden apple, up to 30 points a day. Only food the horse really eats counts (a grown horse at full health turns wheat down).
- **Riding**: a point for every 20 blocks you ride while steering, up to 60 a day. The horse needs something in its saddle slot (saddle, bridle, saddlebags or pack saddle): riding a horse with nothing to steer it, which wanders where it likes, doesn't count. A Bridle makes riding count half again as fast.

Full care with no bonuses is 114 points a day, so a horse becomes Loyal on the fifth day. The caps count points after any bonus, so the Bridle or the RPG Riding skill fills a day's cap sooner but never raises it.

**The Horse Whistle** (a copper ingot and two iron nuggets) calls your most bonded horse that is Loyal or better, within 96 blocks and in a loaded chunk (one with no rider, and not on someone else's lead). A horse that can walk to you comes at a canter, looking for a way for up to 20 seconds; one farther than 40 blocks, or with no way through, is brought to a free spot a few blocks behind you, never into a wall or water. The whistle can't reach horses in unloaded chunks.

The bond's speed, jump and health bonuses are put back on the horse every time it loads, so they never pile up. A bonded horse that loads at full health is filled back up to its bonus, since vanilla trims saved health before the bonus is back.

## Gear

| Item | Slot | What it does | Recipe |
|---|---|---|---|
| **Saddlebags** | saddle (horse) | a saddle with 6 pack slots | leather, saddle, leather over two bundles (any colour) |
| **Bridle** | saddle (horse, donkey, mule) | ride with no saddle; riding grows the bond 1.5x as fast; +1 calm | leather around an iron nugget, string below |
| **Pack Saddle** | saddle (donkey, mule) | a full 15-slot pack with no chest; wicker panniers on the animal | stick, leather, stick over barrel, leather, barrel |
| **Caparison** | body (horse) | 2 armor, dyeable cloth (dye it like leather armor, wash it in a cauldron) | 6 wool and a string |
| **Leather Barding** | body | 4 armor | 7 leather and 2 string |
| **Mail Barding** | body | 6 armor | 4 iron chains and 3 iron ingots |
| **Plate Barding** | body | 10 armor, 2 toughness, a little knockback resistance | Leather Barding inside 6 iron ingots and an iron block |
| **Jousting Lance** | hand | the couched lance (below) | an iron ingot tip, two sticks and a leather grip, corner to corner |

All barding renders on the horse. Pack slots come from what the animal wears, never from its breed: saddlebags give a horse 2 columns (6 slots), a pack saddle or a chest gives a donkey or mule 5 columns (15 slots), and wearing both keeps 15. Changing tack while the horse's menu is open closes the menu (open it again to see the new slots), and taking off saddlebags or a pack saddle drops what no longer fits at the animal's feet. Llamas, camels and undead horses keep vanilla's packs. A donkey with a chest that also wears a pack saddle shows the panniers over the chest.

## Stables

- **Horse Stall** (fences, planks and a hay bale): right-click it while riding a horse you own, or while leading one on a lead within 10 blocks, and the stall becomes that horse's home: it stays within six blocks of it. A stall holds one horse; your own horse already living there moves out. The village's horses keep their stalls, and a resident's or the village's horse can never be stalled by a player. With an empty hand it tells you whose stall it is.
- **Hay Trough** (planks and a hay bale): holds four servings. Fill it with wheat (one serving) or a hay bale (all four); use it with an empty hand to see how full it is; comparators read it. Every 30 seconds, each stalled horse that is hurt or still a foal walks to the nearest trough with hay within six blocks of its stall and eats: two health back, or a minute off growing up. One time in three a serving is used.
- **Foals grow up at home.** A foal born to a stalled horse (horse, donkey or mule) shares its parent's stall, so it eats from the trough and the stablehand looks in on it. When a player's horse and a village horse have a foal, the player keeps it.
- **Saddle Rack** (leather, planks and sticks): the stablehand's workstation. An unemployed villager near one becomes a **stablehand**. During work hours the stablehand tops up each Hay Trough once a day and looks in on each stalled horse every two minutes or so (a pat, a little health back, hurt ones first), giving up on a chore it can't reach after 30 seconds.
- **Horse Papers**: the stablehand sells horses as papers. Use them on the top of a block with room and the horse (a breed, a donkey or a mule) is there: grown, tame and yours.

The stablehand's trades (three offers from each level):

| Level | Sells | Buys |
|---|---|---|
| Novice | Grooming Brush 3, Bridle 5 | 20 wheat, 18 carrots |
| Apprentice | Rouncey papers 10, saddle 6, Hay Trough 4 | 6 leather, 10 apples |
| Journeyman | Saddlebags 12, Caparison 8, Palfrey papers 14, Donkey papers 6 | 4 hay bales |
| Expert | Leather Barding 10, Mail Barding 18, Horse Whistle 10, the village's own horse 18 | 3 golden carrots |
| Master | Plate Barding 28, Jousting Lance 16, Destrier papers 32, Pack Saddle 8, Mule papers 10 | |

Prices are emeralds. The expert's own horse depends on the stablehand's home: a courser in plains (and jungle and swamp) villages, a desert horse in the desert, a steppe pony in the savanna, a fjord in the taiga and a draft horse in the snow.

**Village stables.** All five village types can build a stable on their outer streets (plains timber, desert sandstone under acacia, savanna acacia, taiga spruce under dark oak, snowy spruce under a steep roof): three stalls under one roof, each with its own trough, a tack corner with the Saddle Rack, and a fenced yard with an open gap to the street (villagers can't open fence gates, so the stablehand and the knights come and go through it; the stalls keep the horses close). Its three horses settle into the stalls when they first load, each taking a breed the village keeps, and belong to the village.

## Mounted combat

**The Jousting Lance** is a couched lance built on vanilla's spear charge. Hold use while galloping and the hit scales with how fast you close on the target: vanilla's `base + floor(speed x multiplier)` with a 1.6 multiplier, so a 12 blocks-a-second gallop lands about 20 damage where an iron spear lands 12. It only lands above 7 blocks a second, faster than a sprint on foot (about 5.6), so it is a horseback weapon; a fast hit also knocks the target back (above 7) and off its own mount (above 9). Your horse's bond adds 2.5% per tier (10% when Devoted), but only for the horse's bond partner: a borrowed or stolen horse fights for nobody. The left-click jab stays vanilla's.

**Steadier mounted shots.** Anything a rider (a player or a resident) fires through vanilla's projectile aim, bows and crossbows above all but also thrown tridents, snowballs, potions and pearls, is steadier from horseback: the spread shrinks by 10% plus 10% per bond tier (at most 75%), and 50% plus 10% per tier of the horse's own movement is taken out of the shot (at most 90%), so arrows go where you look instead of drifting with the gallop.

## Village riders and horse deeds

- **Knights ride the night watch.** When their village has a stable anywhere in it (village stables stand on the outer streets, often 80 blocks or more from the bell), knights on the night watch walk to a free stable horse of their own village (the village's or a resident's, never a player's), mount it and ride their patrol. A squad that is all on horseback trots (1.4x); a mixed squad keeps the walkers' pace. When the watch ends they ride back to the stall and get off, or get off where they are if the ride takes too long (a minute, more when the stable is far). The walk to the horse is given time to match its length too. Knights never mount for a raid: that is no moment to walk to the stable.
- **Loose stable horses drift home.** A village horse left more than 8 blocks from its stall, with no player within 32 blocks to see it, is moved back beside its stall: from any distance when no player took it out (a knight left it after the watch, it wandered or it bolted), and from up to 48 blocks when a player did.
- **Companions ride along.** When you get on a horse, a recruited companion looks once for a spare horse of yours within 8 blocks (tame, grown, no rider, not on a lead) and mounts it; they get off when you do.
- **Stole a Horse** (bad deed): riding or leading a resident's or the village's horse more than 48 blocks from its stall. You are told at once ("This horse belongs to Millbrook. Taking it this far from its stable is theft."). Riding or leading a village horse more than 8 blocks from its stall makes you the one who took it, and that is saved on the horse until it is home, so there is no getting round it: hopping off at 47 blocks and straight back on, coaxing it on with a golden carrot and mounting it out there, or leaving it out for a while and coming back for it later are all still theft.
- **Lost horses.** A village horse a player took out and left more than 48 blocks away, with nobody riding or leading it for over a minute, is lost: anyone else who takes it up is told "This horse is a long way from its stable in Millbrook. Bring it home and they'll be glad of it." (and riding it is not theft for them). For the player who left it there, picking it up out there again is theft.
- **Returned a Horse** (good deed): bring a stolen or lost horse within 8 blocks of its stall. The thief, or the player who took it out and left it, bringing it back just clears the flags, and each horse earns the deed at most once a game day, so leading one out and back is no way to farm standing.
- A horse you stabled yourself is yours to ride anywhere.

## RPG add-on: the Riding skill

With the Village Friends RPG (1.1.0, which needs Village Friends 2.29.0 or later), **Riding** is the 17th skill. It trains from distance on horseback (a point per 5 blocks, donkeys and mules too), from caring for your horse (half a point for every bond point grooming or feeding earns) and from couched lance hits (6 each). Each level gives +0.2% horse speed while you ride, +1% bond growth, +0.4% lance damage and 0.6% steadier mounted aim (+10%, +50%, +20% and +30% at level 50). Stablehand asks for these through `StablehandEvents.RIDING_BONUS` and applies them itself, so without the add-on nothing changes.

## Not-So-Vanilla Mobs (optional): horses that spook

A horse's **calm** is its bond tier (0 Wary to 4 Devoted) plus 1 under a Bridle.
- **Challenger bosses** (the `villagefriends:challengers` entity tag, which lists Not-So-Vanilla Mobs' ten challengers and is read only when `nsvmobs` is installed) frighten every horse within 16 blocks: calm 0–1 bolts, or throws its rider; calm 2–3 rears ("Your horse shies at the ..."); calm 4 and up stands its ground with a challenge neigh ("Your horse stands its ground against the ...").
- **Ordinary monsters** within 4 blocks only bother a horse someone cares for (a bond partner, or a horse in a player's stall) that is still at calm 0: it bolts, or rears under a rider. Wild horses and the village's stable horses keep vanilla's behaviour, so zombies at night don't chase the stable horses out of their stalls.
- A horse reacts at most once every 10 seconds. A stalled horse bolts only within six blocks of its stall, and a horse under a resident never spooks.

## Turning Seasons (optional)

`data/villagefriends/seasonal_spawns/horses.json` (written by `breeds.py`) makes horses, donkeys and mules turn up 1.6x as often in spring, the foaling season, 0.9x in autumn and 0.6x in winter. Only Turning Seasons reads it; without it nothing changes.

## How it works

- **No new horse.** Everything is saved on vanilla horses, donkeys and mules as Fabric attachments (`StableData`): `BREED` (breed and coat, synced to clients for the coat), `BOND` (partner, points and the day's care counters, server only), `STALL` (`StallHome`: the stall, its village, the keeper (`player:<uuid>`, a resident id or `village`) and the theft flags) and `MOUNT_ORDER` (why a resident is riding). Horse Papers carry the `villagefriends:horse_papers` component.
- **One start-up call.** `Stablehand.register()` in `VillageFriends.onInitialize` registers the attachments, reads the two data tables from the classpath (`StableTable.load`), the component, blocks, items, then the four features: `BreedFeature`, `GearFeature`, `YardFeature`, `RideFeature`. `StablehandClient` registers the client side.
- **Breeds.** `ENTITY_LOAD` gives a breed to a `Horse` that has none (`BreedPicker` by biome keywords, `BreedRolls` for stats). Horses tagged `villagefriends.stable_horse` are left to the yard, which settles them into a free stall by a block scan the tick after they load (retrying on the yard tick, giving up after three tries with a biome breed). Foals get theirs in `AnimalBreedingMixin` (`BreedHooks.bred`, before the foal joins the world: `Inheritance` picks the breed and blends the stats), which also gives the foal its parent's stall. The coat is swapped on the client: `HorseRenderStateMixin` copies `BREED` into the render state and `HorseCoatMixin` returns the breed's texture (`HorseCoats`).
- **Bond.** `HorseEatingMixin` (feeding), the brush's `UseEntityCallback` and a once-a-second ride sample feed `BondMath.gain`, which applies the daily caps after the multiplier. Tier bonuses are transient attribute modifiers re-applied on `ENTITY_LOAD` (a bonded horse that loads at its bond-less maximum is filled back up). The whistle raises the called horse's path length while it walks over (vanilla plans only 16 blocks for a horse) and puts it back after.
- **Pack slots.** `HorseEquipMixin` (`LivingEntity.onEquipItem`, HEAD) resizes the pack in the same call that changes the tack: spill what no longer fits, copy the rest, clear the old container. `HorsePackMixin` gives the column count (`ChestedHorsePackMixin` for donkeys and mules), saves a pack vanilla wouldn't (a chestless donkey's or mule's) and resizes once more before the horse menu is built, so the menu never has more slots than the container.
- **Combat.** `StabAttackMixin` boosts a couched stab (`CombatHooks.stab`) and fires `LANCE_HIT`; `ProjectileSteadyMixin` narrows the spread (`CombatHooks.aim`) and takes the horse's movement out of the shot (`CombatHooks.shot`).
- **Riders.** A villager on a tame horse steers it: its navigation is the horse's, so the ordinary walk target moves the horse. `Mounts.mount` drops the rider's own on-foot path before seating them: vanilla keeps ticking a rider's own navigation, which steers through the horse's move control and would walk the horse back along that path once the horse's own path is done. `Mounts.update` runs from the routine chain in `ResidentRoutines` (before `StableWork`, the stablehand's chores); `GuardController` and `GuardPatrols` read `Mounts.pace` and `Mounts.spacing`; `CompanionController` calls `Mounts.companion` and `Mounts.dismount`; two `Mounts.caravan` checks (`ResidentRoutines` and `VillagerCompanionMixin`) switch a caravan guard's routine and brain off. While a resident rides, the horse gets a transient +32 follow range (`villagefriends:rider_reach`), because the horse's navigation plans the rider's paths and a horse's own 16 blocks would turn patrol legs into short hops; dismounting removes it, and `Mounts.loaded` (on `ENTITY_LOAD`) puts it back when a mounted resident and their horse load again. Knights find their village's stable horses through the village record around their bell (`VillageSettlements`), not a fixed reach, and `MountedPace.errandTicks` stretches the walk to the horse and the ride home with the distance.
- **Deeds and spooking.** `HorseDeeds` checks stable horses every 40 ticks (`TheftRule`) and sweeps for drifting horses every 200, recording `STOLE_HORSE` and `RETURNED_HORSE` through `Deeds.record`. Who took a horse out is saved in its `StallHome` (`takenBy`), so a restart or a long wait never turns its taker into its finder. `Spook` checks ridden horses once a second and every horse gets a `SpookGoal` for bolting (`SpookRule` decides). Nothing in Stablehand runs every tick per horse, and no search loads a chunk.
- **Optional mods.** Village Friends never imports the RPG add-on; the add-on's `Riding` listens to `StablehandEvents` (`BOND_GAINED`, `LANCE_HIT`) and answers `RIDING_BONUS`. NSV challengers come only through the optional entity tag. There are no mixins into other mods.

## Files

| Piece | Code or data |
|---|---|
| Start-up, data, items, blocks | `stable/Stablehand`, `stable/data/*` (`StableData`, `StableTable`, `StableItems`, `StableBlocks`, `HayTroughBlock`, `StableComponents`, `StableTags`, the records) |
| Public API | `stable/api/Horses`, `PackAnimals`, `Stables`, `Riders`, `StablehandEvents` |
| Breeds and bond | `stable/breed/*` (`Breeds`, `BreedPicker`, `BreedRolls`, `Inheritance`), `stable/bond/*` (`BondMath`, `Bonds`, `Grooming`, `Whistle`); client `client/breed/HorseCoats` |
| Gear and combat | `stable/gear/*` (`Tack`, `PackCapacity`, `PackHooks`, `LanceMath`, `ArcheryMath`, `CombatHooks`, `GearText`); client `client/gear/GearClient` |
| Stables | `stable/yard/*` (`Stalls`, `Troughs`, `StableWork`, `StableHorses`, `Papers`, `StallRules`, `StableSites`); client `client/yard/YardClient` |
| Riders, deeds, spooking | `stable/ride/*` (`Mounts`, `MountedPace`, `HorseDeeds`, `TheftRule`, `Spook`, `SpookRule`) |
| Mixins | `stable/mixin/*`, `client/mixin/HorseCoatMixin`, `HorseRenderStateMixin` (configs `villagefriends.stablehand.mixins.json` and its client twin) |
| Data tables | `data/villagefriends/villagefriends/stablehand/breeds.json`, `gear.json` (compiled) |
| Tools | `tools/stablehand/stablehand.py` (runner: `--check`, `--preview`, `--only`), `breeds.py`, `gear.py`, `yard.py` (`--boxes`, `--check`), `riders.py`, `lang.py`, `kit.py` |
| Stable buildings | `tools/village_design/buildings/stable.py` and `buildings/<type>/stable.py`, blueprints `tools/village_blueprints/**/stable.json`, pool entries in `tools/village_layouts/plains.json` and `<type>.lots.json` |
| Dialogue | `tools/dialogue/lines/stablehand.txt` (95 lines: the stablehand's work talk, station hints and jokes, `village.horses`, and the two horse deeds) |
| RPG | `rpg/src/main/java/dev/villagefriends/rpg/Riding.java` |
| Tests | `src/test/java/dev/villagefriends/stable/*Test.java`; `src/gametest/java/dev/villagefriends/StablehandGameTest.java`, `StableTestKit`, `Stable{Breed,Gear,Yard,Rider}Scenes` |

Never hand-edit a compiled JSON or PNG (`breeds.json`, `gear.json`, coats, gear art, recipes, trades, `challengers.json`, `seasonal_spawns/horses.json`): change the Python and rerun `python tools/stablehand/stablehand.py`, then `--check`. Previews go to `build/previews/` with `--preview`.

## Add a breed

1. Add a row to `BREEDS` in `tools/stablehand/breeds.py`: `id`, `name`, the `health`, `speed` and `jump` ranges (keep inside vanilla's reach: health 10–40, speed 0.1–0.36, jump 0.35–1.05), `spawns` (biome keyword and weight; keywords are listed at the top of the file), `extra_spawns` for biomes where vanilla has no horses (keyword, weight, smallest and largest group; desert and badlands rows become sand herds), the vanilla `markings` it may wear, `coats` and the village types that keep it in their stables (`village`).
2. Give it a palette in `PALETTES` (and any extra coats in `VARIANTS`; `coats` must match their count). Each coat is painted on the vanilla horse's UV layout from these ramps, adult and foal.
3. Run `python tools/stablehand/stablehand.py`. It writes `breeds.json`, the coat PNGs and the breed's language key (`stablehand.breed.<id>`, from `name`). Then `--check`, and `--preview --only breeds` to look at the flat UV sheets and the 3D sheet in `build/previews/`.
4. To sell its papers, add `papers:<id>` to a level of `TRADES` in `tools/stablehand/yard.py` (or make it a village's own horse in `LOCAL_PAPERS`) and rerun.
5. `StableTableTest.thereAreEightBreedsWithTheirOwnIds` lists the breed ids: add the new id there. Then run the unit tests (`gradlew :test --tests "dev.villagefriends.stable.*"`).

No Java changes are needed: everything reads the table.

## Pack-animal API

`dev.villagefriends.stable.api.PackAnimals`, for Kingsroads & Caravans and other mods. All static, server side, safe to call whether or not Stablehand's other features are in use.

**Pack slots.** An animal's pack comes from what it wears, never from its breed or bond: saddlebags give a horse 6 slots, a pack saddle gives a donkey or mule 15 (no chest needed), and a chest gives a donkey or mule vanilla's 15. The pack resizes in the same call that changes the tack, so fitting a pack saddle and loading goods in one server task works. Goods are saved with the animal, chest or no chest. Taking the tack off spills what no longer fits at the animal's feet, and an open horse menu closes when the pack resizes (open it again).

**Guards.** `mountGuard` seats a resident for a caravan: while mounted, Village Friends switches off their daily routine and their villager brain, and the caller steers with `guard.getNavigation().moveTo(x, y, z, speed)`, which drives the horse. A knight or archer attacked on the road still fights first. `dismountGuard` hands them back to their routine.

```java
var mule = PackAnimals.spawnPackAnimal(level, pos, "mule");          // tamed adult mule with a pack saddle
var left = PackAnimals.load(mule, List.of(new ItemStack(Items.WHEAT, 64), new ItemStack(Items.IRON_INGOT, 20)));
var horse = PackAnimals.spawnHorse(level, pos.east(2), "destrier");
if (PackAnimals.mountGuard(knight, horse)) knight.getNavigation().moveTo(x, y, z, 1.2);
List<ItemStack> goods = PackAnimals.unload(mule);                     // at the market
```

| Method | What it does |
|---|---|
| `canCarry(animal)` | True for an adult, tamed horse, donkey or mule whose gear gives it pack slots (saddlebags, pack saddle or chest) |
| `capacity(animal)` | Pack slots it has now (columns x 3), 0 if none |
| `fitPackSaddle(animal)` | Tames (no owner) and fits a pack saddle on a donkey or mule, dropping any saddle it wore. False for other animals or babies |
| `load(animal, goods)` | Puts copies of the goods into the pack, merging stacks; returns what did not fit (never null) |
| `unload(animal)` | Empties the pack and returns everything that was in it |
| `contents(animal)` | A copy of what is in the pack, in slot order, without empties |
| `spawnPackAnimal(level, pos, kind)` | Spawns a tamed adult donkey or mule (`"donkey"` / `"mule"`) wearing a pack saddle at `pos`; null for any other kind |
| `spawnHorse(level, pos, breed)` | Spawns a tamed, saddled adult horse of a breed (null or unknown = the biome's pick) at `pos`, with no owner |
| `mountGuard(guard, horse)` | Seats a resident on a horse (order `"caravan"`) until `dismountGuard`. Their routine and brain stay off, so they stay where the caller puts them; `guard.getNavigation().moveTo(...)` drives the horse at its own speed times the modifier (1.0 to 1.6 is a walk to a canter). False if the horse is not a tame adult, already has a rider, or the villager is a baby |
| `dismountGuard(guard)` | Takes a resident off their horse and clears the caravan order; their routine resumes on its next update |

The other facades: `Horses` (`breed`, `pickBreed`, `assignBreed`, `breedName`, `breeds`, `bondPoints`, `bondTier`, `bondPartner`, `addBond`, `bondable`), `Stables` (`stableNear`, `stall`, `stallOf`, `stalledHorses`), `Riders` (`mount`, `dismount`, `riding`, `order`) and `StablehandEvents` (`BOND_GAINED` with the source `groom`, `feed`, `ride` or the label given to `Horses.addBond`, default `api`; `LANCE_HIT` with the boosted base damage and the horse's speed in blocks a second; `RIDING_BONUS`, which add-ons answer with an extra fraction per `Aspect`). The entity tag `villagefriends:challengers` lists the bosses that spook every horse; the entity tag string `villagefriends.stable_horse` marks a stable template's horses until they settle.

## Known limits

- The whistle reaches only horses in loaded chunks.
- While a village horse is stolen and far away, a player can stall their own horse in its empty stall; when the village horse comes back, both horses call that stall home.
- A loose village horse drifts home only while its stall's chunk is loaded; until then it waits where it is.
- Only a horse a player took out and left can be lost and found. A player who mounts a village horse more than 48 blocks out that nobody took (a knight got off it there a moment ago) is riding it away from its stable, which is theft; bringing it back clears the flag.
- A rider pulled off by a knockout or the village alarm leaves the harmless `villagefriends:rider_reach` follow-range bonus on the horse until it next unloads (it is never saved).
- Saved pack slots past the current column count are dropped on load; only a future change to `gear.json` could cause it.

## Testing

- Unit tests (pure logic, JUnit 5, `src/test/java/dev/villagefriends/stable/`): `StableTableTest` (both tables), `StableBreedsTest` (rolls, the biome picker, inheritance, coat sizes), `StableBondTest` (tiers, caps after the multiplier, Loyal on day 5, the bridle), `StableGearTest` (pack capacity for every animal and gear, lance and archery maths, tooltips, gear assets), `StableYardTest` (stall rules, troughs, settling, foals' stalls, village breeds, the trade data) and `StableRidersTest` (mounted pace, errand time, every theft verdict, spooking). `DeedScoringTest`, `DialogueBankTest`, `RoutineTest`, `HouseCatalogTest` and `GuardDutyTest` cover the shared parts; the RPG's `RpgBalanceTest` covers Riding. Run them all with `gradlew test :rpg:test`. Use `:test --tests <Class>` for one root class: a bare `test --tests` also selects `:rpg:test`, which then fails with "No tests found".
- `python tools/stablehand/stablehand.py --check`, `python tools/stablehand/yard.py --check`, `python tools/dialogue/dialogue.py --check` and `python tools/create_village_structures.py --check`.
- The client game test `StablehandGameTest` runs four scenes and reports every failure at once (one failing scene doesn't stop the others): breeds (a destrier x courser foal's breed, stats and foal coat, the bond to Loyal, the whistle from 30 and 58 blocks, the brush, a Loyal horse keeping its bonus health through a save and load; screenshots `stablehand-breeds-lineup`, `stablehand-breeds-foal`), gear (plate barding and saddlebags, a save and load, the same-tick resize and spill, a blue caparison, donkey and mule packs, the lance hook and a live charge), yard (stalling by riding and by lead, the trough, papers, the plains stable template settling three horses, the stablehand's trades) and riders (knights riding the night watch and drifting home, a companion, a caravan guard, theft and its return, spooking). Run it with `gradlew runClientGameTest -Ptests=StablehandGameTest -PtestHeap=2560m` (add `-PwithRpg` to load the RPG add-on too). It is not part of the default run.

