# Hearth & Harvest: cooking for the village

Version 2.27 adds cooking. Three kitchen stations (a cooking pot over a fire, a clay oven and a prep table), six medieval crops, 63 new dishes (68 with the five the mod already had) from one data table, tiered Well Fed buffs, family recipe cards, and residents for whom food matters: they eat real dishes at home, the tavern serves and sells the cook's dish of the day, everyone has a favorite dish, picnics and gatherings are better with one, and birthday parties serve a cake.

## Where things live

| Piece | Code or data |
|---|---|
| The dish table (every dish, kitchen ingredient and recipe) | `tools/hearth/dishes.tsv`; crops `crops.tsv`; mob ingredients `ingredients.tsv` |
| Compiler for the tables | `python tools/hearth/hearth.py` (`--check`, `--stats`) |
| Item and crop art | `python tools/hearth/sprites.py` (`--check`, `--preview`) |
| Station models, textures and the screens' art | `python tools/hearth/stations.py` (`--check`, `--preview`) |
| Runtime dish table | `src/main/resources/villagefriends/hearth/dishes.json` (compiled; read at start-up by `hearth/Dishes`) |
| Station recipes | `data/<namespace>/hearth_recipe/*.json` (compiled from the table, loaded by `hearth/HearthRecipes`) |
| Everything starts at | `hearth/Hearth.register()`, one call in `VillageFriends` |
| Tastes, menus, gift values, Well Fed times (pure, unit-tested) | `hearth/Tastes`, `hearth/Cookbook`, `hearth/Dish`, `hearth/Dishes` |
| Items and crops | `hearth/HearthItems` (`DishItem`, `HearthCrop`), `hearth/RecipeCardItem` |
| Stations | `hearth/HearthBlocks`, `hearth/StationBlock` (`Pot`, `Oven`, `Prep`), `hearth/StationBlockEntity`, `hearth/StationMenu`; client `client/StationScreen` |
| Well Fed | `hearth/WellFed` (the effect and the `villagefriends:well_fed` consume effect every dish carries), `mixin/WellFedHungerMixin` |
| The village | `hearth/HearthVillage` (favorites, gifts, family recipes, picnics, the party cake, the keeper's dish of the day), `hearth/HomeMeals`, `hearth/HearthFarms`, `mixin/TavernSpecialMixin` |
| Other mods | `hearth/HearthCompat` (Not-So-Vanilla Mobs drops), `hearth/HearthSeasons` (Turning Seasons), `hearth/HearthApi` and `hearth/HearthEvents` (hooks), the RPG add-on's `rpg/Cooking` |
| Dialogue | `tools/dialogue/lines/hearth.txt` (282 lines) |
| Animations | `tools/animations/village_life/meals.py` (standing home meals; seated meals use the Tavern pack) |

## The stations

| Station | Where | Slots | Needs |
|---|---|---|---|
| **Cooking Pot** | On top of a lit campfire, soul campfire, fire, lava or magma block (the block tag `villagefriends:hearth/heat_sources`; a campfire must be lit) | 6 ingredients, the vessel (bowl or glass bottle), output | Heat from below |
| **Clay Oven** | Anywhere | 6 ingredients, fuel (anything that burns in a furnace), output | Fuel, burnt like a furnace |
| **Prep Table** | Anywhere | 6 ingredients, output | Nothing |

Crafting: the **Cooking Pot** from five iron ingots and two iron nuggets (nuggets on top for the handles, ingots in a pot shape), the **Clay Oven** from clay balls and bricks over a row of stone, and the **Prep Table** from an iron ingot (the knife), three wooden slabs and two fences. Recipes in `tools/hearth/hearth.py` (`STATION_CRAFTING`).

Ingredients go in any order, one per slot; a batch uses one from every filled slot, so a stack in each slot makes several batches one after another. Buckets and bottles come back (a milk bucket leaves its bucket in the slot). Pot dishes also use one bowl or bottle from the vessel slot. The pot bubbles and steams while it cooks and shows a stew inside when it holds anything; the oven glows, smokes and lights the room while it burns. Hoppers fill the grid from above and the vessel or fuel slot from the side, and take dishes out from below; a comparator reads how full the output is.

**The screen** has a recipe book beside it (toggle it with the book button). It lists every recipe for that station: hover one for what it makes, its Well Fed tier and time, what it needs and how long it takes; click it to fill the grid from your inventory (shift-click for as many batches as you have, up to sixteen). Recipes you're missing something for are tinted red. Family recipes you haven't learned are sealed cards.

**Family recipes** (12 of them, such as Harvest Stew, Celebration Cake and Steak and Onion Pie) only cook for someone who knows them. The cook is whoever last opened the station. Learn one from a **Recipe Card**: right-click it. Players in Creative can cook everything, and `/hearth learn all` teaches every family recipe.

## Crops

| Crop | Seed | Grown in |
|---|---|---|
| Onion | Onion Seeds | plains, desert, savanna, taiga, homesteads |
| Cabbage | Cabbage Seeds | plains, snowy, taiga, homesteads |
| Barley | Barley Seeds | plains, savanna, snowy, taiga |
| Garlic | Garlic Clove | plains, desert, savanna, homesteads |
| Leek | Leek Seeds | plains, snowy, taiga, homesteads |
| Kitchen Herbs | Herb Seeds | plains, desert, taiga, homesteads |

They grow like wheat (eight stages drawn in four) on farmland and drop their seeds; a ripe crop drops 1–3 of the produce and extra seeds (Fortune helps). **Village fields are sown with them:** about a third of the vanilla crops in every village farm, kitchen garden and greenhouse of a type are swapped for that type's Hearth crops as the village is built (the `<type>_<base>_fields` processor lists that `hearth.py` writes into `tools/village_layouts/<type>.hearth.json` and points the crop-bearing templates at), and the farmstead and the pariah's garden out in the wild use `homestead_fields`. **Farmers** keep a few seeds of their village's crops (`HearthFarms`, once a day) and plant them with vanilla's own farming, since the seeds are in `minecraft:villager_plantable_seeds`. Farmers **sell** the seeds (Onion, Cabbage and Herb Seeds at Novice; Barley, Leek and Garlic at Apprentice) and buy the produce, through vanilla's farmer trade tags.

Tags: item `c:crops`, `c:crops/<crop>`, `c:seeds`, `c:seeds/<crop>`, `villagefriends:hearth/crops`, `villagefriends:hearth/seeds`; block `minecraft:crops` (so Turning Seasons and bees treat them as crops), `minecraft:bee_growables`, `minecraft:maintains_farmland`, `villagefriends:hearth/crops`.

## Dishes and Well Fed

Five kitchen ingredients feed the dishes: **Flour** (wheat, prep table), **Butter** (a milk bucket makes three), **Farmhouse Cheese** (milk in the pot), **Pastry** (flour and butter) and **Trenchers** (bread plates, baked). The 68 dishes: 27 from the pot (pottages, stews, soups, porridge, frumenty, mulled cider, posset), 31 from the oven (breads, pies, pasties, roasts, tarts, honey cakes, the Celebration Cake, smoked fish) and 10 from the prep table (trenchers, salads, cheese boards, a picnic bundle, sauerkraut, pickled onions). The five dishes the mod already had (Hearty Stew, Fresh Village Bread, Shepherd's Pie, Ploughman's Lunch, Apple Tart) keep their items and recipes and gain station recipes and Well Fed.

**Well Fed** I, II or III (from the dish's tier) lasts 1½ to 4 minutes:

| Tier | Effect |
|---|---|
| I | Hunger drains 15% slower |
| II | 25% slower, and half a heart back every 12 seconds |
| III | 35% slower, and half a heart back every 8 seconds |

It never stacks: a better meal replaces a lesser one and another helping of the same tier only tops the time up (vanilla's own effect rules). A **fine** dish (see the RPG add-on) says "Fine" in its name, glints, gives Well Fed half as long again and is worth a little more as a gift. Tooltips show each dish's tier and time.

**Adding a dish:** add a row to `dishes.tsv` (its header explains every column), then run `python tools/hearth/hearth.py` and add a sprite in `tools/hearth/sprites.py` (its `--check` fails until you do). The row gives the item, its food values, its Well Fed tier and time, its station recipe, the animation kind residents use for it (`serve`), when residents eat it (`meals`: breakfast, lunch, supper, tavern, picnic, party, winter) and who tends to love it (`likes`: personalities, jobs or `child`). Flags: `secret` for a family recipe, `needs:<modid>` for a recipe that only loads with another mod, `existing` for an item the mod already registers, `ingredient` for kitchen ingredients.

## The village

- **Favorite dishes.** Every resident has one, decided from their id, personality, job and age (children love sweet things), and it never changes. A gift of it is worth 18 friendship (more than their favorite thing) and they light up; any other dish is a good gift too (8–12 by tier, a little more if fine). They talk about it ({dish} in dialogue), stare when you hold it, and react to other dishes you carry. The Ledger and the conversation window's hints show it once you're acquaintances.
- **Meals at home.** At breakfast, lunch at home and supper, once a resident is back at their own house they eat a real dish that suits the meal and them (now and then their favorite), dish in hand, with bites, crumbs and a pause to chew; the status line says what they're eating ("Having supper · eating onion pottage"), and so do they if you talk to them.
- **The tavern.** The cook's dish of the day and the tavern's lunch and supper come from the dish table's tavern dishes (a rotation of 18 that keeps stews, pies and breads taking turns), served at the tables as before. The tavern keeper **sells** today's dish (one emerald plus one per Well Fed tier, eight a day) and takes yesterday's off the list.
- **Family recipes.** The first time a resident who is at least a Friend (level 4) talks to you, they hand you their family recipe on a Recipe Card, with a story about who taught them. Each resident's is the secret dish that suits them best, so different friends give different cards. (The pariah keeps theirs.)
- **Picnics and gatherings** start with any dish as well as bread, an apple or a cookie. Bringing a dish is worth 4 more friendship (8 if it's their favorite) and 2 for every guest at a gathering, once a day, and they remember what you shared.
- **Birthday parties serve a cake:** at cake time the guest of honor and every guest eat a slice of their party cake (their favorite cake, or one that suits them), and every player there gets a slice of it. A Hearth cake given on someone's birthday counts as a cake.

## For other features and mods

- **Fish:** anything in the item tag `villagefriends:cooking/fish` (`HearthApi.FISH`) goes into the fish dishes (Fisherman's Stew, Fish Pie, Fish and Herb Soup, Smoked Fish). It holds cod and salmon, raw and cooked.
- **Dishes:** a row in `dishes.tsv` (in Village Friends), or `HearthApi.registerDish(Dish)` during mod initialization.
- **Recipes:** data packs (`data/<ns>/hearth_recipe/*.json`, format in `HearthRecipes`; `fabric:load_conditions` work) or `HearthApi.registerRecipe(CookingRecipe)` (kept across reloads).
- **Hooks** (`HearthEvents`): `COOKED` (a station finished a batch; change the result), `TAKEN` (a player took food out), `EATEN` (a factor for the Well Fed time). `HearthApi.makeFine`, `isFine`, `dish`, `known`, `learn`, `favorite`.
- **RPG add-on:** the **Cooking** skill. Taking food out of a station trains it (1 per kitchen ingredient, 8–16 per dish by tier); each level makes Well Fed last 1% longer (50% at 50) and gives your dishes a 0.8% chance to come out fine (40% at 50).
- **Not-So-Vanilla Mobs:** its loot tables drop only vanilla items, so with NSV installed Village Friends adds three ingredients: a Raw Boar Haunch from Wild Boars, Brineclaw Meat from the Brineclaw and a Sporecap from Sporelings (`HearthCompat`, through Fabric's loot drop hook, only when `nsvmobs` is loaded). Their four dishes (Boar and Barley Stew, Roast Boar with Apples, Brineclaw Bisque, Sporecap Pottage) load only with NSV and never become anyone's favorite.
- **Turning Seasons** (optional): the crops are in `#minecraft:crops`, which its seasonal growth already covers. `HearthSeasons` reads its season through its public API by reflection (no dependency): in winter one home meal in three comes from the winter larder (dishes with the `winter` meal: sauerkraut, pickled onions, smoked fish, mulled cider, spice cake), and those dishes keep you Well Fed half as long again in winter. Without it nothing changes.

## Verification

- `gradlew :test`: `HearthTest` (the table's size and balance, any-order exact matching, the fish tag, family recipes, no two recipes on one grid and every kitchen ingredient made somewhere, favorites that suit personality, job and age, home meals that fit the meal, the party cake, the tavern menu's rotation, gift values and Well Fed times) and `PatronageTest`. `gradlew :rpg:test`: `CookingSkillTest`.
- `-Ptests=HearthGameTest` cooks a dish at each station through its screen and recipe book (screenshots `hearth-*`), checks Well Fed, the family-recipe lock and card, a favorite-dish gift, a Friend's recipe card, the keeper's dish of the day and a resident eating supper. `CelebrationsGameTest` checks the party cake.
- `python tools/hearth/hearth.py --check`, `tools/hearth/sprites.py --check`, `tools/hearth/stations.py --check`, `tools/dialogue/dialogue.py --check`, `tools/animations/animations.py --check`, `tools/create_village_structures.py --check`.
