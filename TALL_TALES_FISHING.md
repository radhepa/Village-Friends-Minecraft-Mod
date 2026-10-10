# Tall Tales Fishing: fishing with stories behind it

Version 2.28 rebuilds fishing. When a fish bites, a catch-bar minigame starts; 84 fish (80 new, plus vanilla's four) bite by kind of water, the land around it, the time, the weather and (with Turning Seasons) the season; nine of them are legends that residents tell tall tales about. Rods, bait and tackle change the odds, the Angler's Journal records every species and your biggest catch, a Trophy Mount hangs one on the wall, villages near water build a fishing dock where their fisherman fishes, and every season each village holds a fishing contest at the tavern.

## Where things live

| Piece | Code or data |
|---|---|
| The fish table | `tools/fishing/fish.tsv` (the header documents every column) |
| Compiler | `python tools/fishing/fishing.py` (`--check`, `--stats`): the runtime table, tags, recipes, the fishmonger's trades, names |
| Fish art and journal silhouettes | `python tools/fishing/sprites.py` (`--check`, `--preview`) |
| Gear, the trophy mount, the minigame and journal screens | `python tools/fishing/art.py` (`--check`, `--preview`) |
| Runtime fish table | `src/main/resources/villagefriends/fishing/fish.json` (compiled; read at start-up by `fishing/FishTable`) |
| Everything starts at | `fishing/Fishing.register()`, one call in `VillageFriends` |
| Pure, unit-tested rules | `fishing/Fish`, `Spot` (water and time as fish see them), `Catches` (what bites, junk and treasure, sizes), `Minigame` (the catch bar), `Gear`, `Journal`, `Tales` (tall-tale wording), `Contest` |
| A fish on the line | `fishing/Angling`, `mixin/FishingHookMixin` and `FishingHookAccess` (vanilla's hook), `fishing/FishingNet` (packets) |
| Items and the mount | `fishing/FishingItems` (fish, bait, tackle, journal, bottle, grilled fish), `fishing/RodItem`, `fishing/TrophyMount` |
| The village | `fishing/Docks`, `fishing/DockAnglers` (residents fishing), `fishing/Contests`, `fishing/FishingVillage` (tall tales, contest talk, bottles) |
| Client | `client/FishingClient` (minigame, contest board), `client/JournalScreen`, `client/TrophyMountRenderer`, `client/AnglingClient` (residents' rods and lines), `client/mixin/FishingUseItemMixin` |
| Other mods | `fishing/FishingCompat` (a Brineclaw from Not-So-Vanilla Mobs), seasons through `hearth/HearthSeasons`, the RPG add-on's `rpg/Angler` |
| Dock designs | `tools/village_design/buildings/docks.py`, listed in `tools/standalone_templates.json` (compiled to `data/villagefriends/structure/dock/<type>.nbt`) |
| Dialogue | `tools/dialogue/lines/fishing.txt` (271 lines) |
| Animations | `tools/animations/village_life/angling.py` (19 clips on the `angling` trigger) |
| Config | `config/villagefriends-fishing.json` (`"minigame": true`) |

## The minigame

When something bites, the server picks what it is and starts the catch bar beside the crosshair. The fish moves up and down a column of water by its own behavior (`smooth` glides, `mixed` changes its mind, `dart` dashes, `sinker` hugs the bottom, `floater` rides the top) and difficulty (0–100). Hold the use button to lift the green catch zone and let go to drop it; it has momentum and bounces off the bottom. While the fish is in the zone the meter on the right fills, otherwise it drains: full is a catch, empty and it gets away. A treasure chest sometimes shows up in the water too (only in open water, as vanilla's treasure): keep it in the zone until it's yours, and the meter doesn't drain while you do. A catch where the fish never left the zone is **perfect** (a slightly bigger fish, more RPG experience).

The client runs the simulation from a seed the server sent (`Minigame`, 20 ticks a second, three steps a tick); the server only accepts a catch that took at least as long as the meter can possibly fill. While it runs the bobber stays under and right-clicking doesn't reel in. Junk is still reeled in the vanilla way, on the dip. `/fishing minigame off` (or `"minigame": false` in the config) goes back to vanilla timing; what comes up still comes from the fish table.

Tuning: with a sensible player, easy fish are always caught and a plain rod can manage most fish, but a legend (difficulty 92–100) needs an Angler's Rod and a Cork Bobber (or the RPG Fishing skill). `FishingTest` checks this with a test player who allows for the zone's momentum.

## Fish

`fish.tsv` holds 84 fish: 27 common, 25 uncommon, 18 rare, 5 epic, 9 legendary. Each says where and when it bites:

- **water**: `river`, `lake` (any other still water), `swamp`, `ocean` (with `warm`, `cold`, `deep` for those oceans), `cave` (underground water below sea level) and `deepcave` (below y 0). Cave fish live only underground.
- **region**: the land around the water, read from the biomes at the bobber and eight points 24 blocks out (`Angling.region`), so a river through the desert is desert water. Regions are defined in `fishing.py` (`REGIONS`): plains, forest, cherry, desert, badlands, savanna, jungle, swamp, snowy, taiga, mountain, mushroom.
- **time** (dawn 5:00–7:00, day, noon 11:00–13:00, dusk 18:00–19:30, night), **weather** (clear, rain, thunder) and **season** (only with Turning Seasons installed; without it seasonal fish bite all year).
- **size** in centimetres: most fish come out small for their kind; luck and perfect catches push them bigger.

What bites is picked by weight (`Catches.weight`): rarity (common 60, uncommon 24, rare 9, epic 3, legendary 0.8), luck (Luck of the Sea, potions, the RPG Fishing skill), bait and the rod. Junk and treasure follow vanilla's own weights. Legends are one per village type (Old Whiskers in the plains, Sunscale in the desert, the River King in the savanna, Rimefin in the snowy north, Old Mossback in the taiga) plus Stormjaw (the deep sea in thunderstorms), the Bog Lantern (swamps), Deepglow (below the world) and the Jade Arowana (jungle). They don't stack, aren't food and are always trophies.

Fish are food (one to three hunger by size; the lionfish stings), smelt, smoke or campfire-cook into **Grilled Fish**, are in `#minecraft:fishes` (so they count as fish caught), and join Hearth & Harvest's `#villagefriends:cooking/fish` through `#villagefriends:fishing/edible`. Five Hearth dishes need particular fish: Jellied Eels (river eel), Crayfish Boil, Stargazy Pie (sardines), Pickled Herring and Herb-Grilled Trout.

## Gear

| Rod | Bait and tackle | Catch zone | Reel | Rare fish |
|---|---|---|---|---|
| Fishing Rod (vanilla) | no | 104 of 568 | normal | normal |
| **Reinforced Rod** (rod + 2 iron + string) | yes | +28 | +10% | +12% |
| **Angler's Rod** (Reinforced + 2 gold + prismarine shard; the fishmonger at Master; contest first prize) | yes | +57 | +20% | +24% |

Click bait or tackle onto a Reinforced or Angler's Rod in your inventory to load it (the same bait tops up to 64, another kind swaps); right-click the rod with an empty hand to take the bait out. Bait is used one per fish; tackle lasts 20 fish.

| Bait | Effect | | Tackle | Effect |
|---|---|---|---|---|
| Bait Worms (dirt + bone meal) | bites 25% sooner; freshwater fish ×1.5 | | Cork Bobber | +32 catch zone |
| Chum (any fish + bone meal) | bites 25% sooner; sea fish ×1.5 | | Lead Sinker | fish move 25% slower |
| Glow Bait (glow berries + worms) | night and cave fish ×2 | | Barbed Hook | the meter drains 40% slower |
| Legend Lure (gold, feather, emerald, glow bait) | legends ×4, epic ×2 | | Treasure Hook | treasure twice as often |
| | | | Spinner | bites 20% sooner |

## The journal and trophies

Craft the **Angler's Journal** from a book and any fish (or buy one). It lists every fish, thirty to a page; an uncaught fish is a dark silhouette and "???". Point at one to read it: rarity, how many you've caught, your record and the day you first landed one, where and when it bites, and its note. A legend whose tall tale you've heard shows the tale before you catch it. The journal is the player attachment `villagefriends:fish_journal` (kept on death, synced to its owner).

A new personal record or a legend comes up as a trophy: it carries its size, who caught it and when (`villagefriends:trophy`), and doesn't stack. The **Trophy Mount** (item frame + 2 planks) goes on a wall; right-click it with a fish to hang it (a trophy shows its size on the plate), empty-handed to read the plate, sneak-right-click to take it down.

## The village

- **Docks.** Once a village's surroundings are loaded, `Docks` looks along its shores (to 16 blocks past its edge) for bank with at least ten blocks of open water in front and builds a dock there in the village's style, driving its pilings down to the bed. Villages without suitable water get none. `/fishing dock build` builds one at the nearest shore.
- **Fishermen and anglers.** A village's fisherman spends his mornings (until 11:00) fishing off the dock, and residents whose hobby is fishing fish there (or from the bank) in their free time: they cast, wait, feel the bite, reel in and hold up the catch, with a real line and bobber. On contest day they fish all day.
- **The fishmonger.** The fisherman's trades now buy fish by the basket and sell bait, tackle, rods, the journal and the trophy mount (three offers a level).
- **Tall tales.** Residents tell rumours of the legends ("the rivers and lakes of the plains", "on rainy nights"); they're true, because they come from the table (`Tales`). A tale you hear goes into your journal. Fishermen tell the most. Messages in bottles (treasure) hold tales too. Land a legend and the village talks about that instead.
- **The contest.** Every season on the 12th each village holds a fishing contest. From 6:00 to 16:30 anything you catch in or near the village counts, and its fishermen and anglers enter too; the standings show in the corner of the screen. At 17:00 the tavern keeper reads out the results, and the winners collect their prizes at the tavern (1st: an Angler's Rod and 8 emeralds; 2nd: 6 emeralds and a Legend Lure; 3rd: 3 emeralds and 8 Glow Bait). Residents look forward to it, more of them sup at the tavern that evening, and they gossip about the winner for days. `/fishing contest start|end|next`.
- **Pets.** Fish are in `minecraft:cat_food` and `minecraft:wolf_food`, and a fish is as good as a pet's favorite treat on its card ("A perch! Biscuit wolfs it down...").

## For other features and mods

- `FishingApi`: tags (`FISH`, `EDIBLE`, `GRILLABLE`, `TREATS`, `LEGENDARY`, `RODS`, `BAIT`, `TACKLE`), `registerFish(Fish)` (bring your own item), `journal(player)`, `land(player, fish, size)`.
- `FishingEvents.TUNE` (adjust a player's minigame before it starts) and `FishingEvents.CAUGHT` (every fish landed).
- Add a fish: a row in `fish.tsv`, then `python tools/fishing/fishing.py` and a sprite in `tools/fishing/sprites.py` (its `--check` fails until there is one).
- **RPG add-on:** the Fishing skill (`rpg/Angler`) still trains on every fish, now with extra experience for rarer fish and perfect catches; each level adds luck, 1.2 pixels of catch zone and 0.6% reel speed.
- **Not-So-Vanilla Mobs:** a sea bite is a Brineclaw 0.4% of the time (three times that on a Legend Lure), hauled out of the water at you.

## Commands (game masters)

`/fishing minigame on|off`, `/fishing bite [fish]` (something bites your hook now), `/fishing catch <fish>`, `/fishing journal fill|clear`, `/fishing contest start|end|next`, `/fishing dock build`.

## Verification

`gradlew.bat :test --tests dev.villagefriends.FishingTest` (and `:rpg:test`), then `gradlew.bat runClientGameTest -Ptests=FishingGameTest -PtestHeap=2560m` (add `-PwithRpg` for the RPG add-on). The game test casts with a real right click and plays the minigame on the client, and photographs the pond, the minigame, the journal before and after, the legend's title, the trophy mount, the dock with its fisherman, the contest board and results, a heard tale and pickled herring.
