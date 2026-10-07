# Village days: routines, weather, working workstations and written dialogue

Version 2.14 gives every resident a day of their own, makes the weather matter, makes every Village Friends workstation do something for players and for the resident who works there, and replaces the handful of lines each personality had with 5,898 pieces of handwritten dialogue chosen from what is actually happening.

## Where things live

| Piece | Code |
|---|---|
| A resident's day and the weather's effect on it (pure, unit-tested) | `routine/Routine.java` |
| Applying routines to the world | `ResidentRoutines` (once a second per resident), `mixin/BrainRoutineMixin`, `mixin/SleepInBedRoutineMixin` |
| Workstation blocks and their memory | `WorkstationBlock`, `WorkstationBlockEntity` (one `villagefriends:workstation` block entity type) |
| What workstations do | `Workstations` (players, the training dummy and archery target, residents at work), `mixin/WorkAtPoiMixin`, `Songbook` |
| Workstation models and art | `tools/workstations/workstations.py` (designs), `tools/workstations/paint.py` (textures) |
| The dialogue bank | `tools/dialogue/lines/*.txt`, `tools/dialogue/questions/*.txt`, compiled by `tools/dialogue/dialogue.py` to `data/villagefriends/villagefriends/dialogue.json` |
| Choosing lines and questions (pure, unit-tested) | `talk/Talk.java`, `talk/DialogueBank.java` |
| Reading the world for dialogue; offers' effects | `TalkWorld` |

## Daily routines

`Routine.day` builds a resident's day from their profile ID (as a seed), job, personality, age and the day number; `Routine.plan` picks the part of the day for the current time and lets the weather change it. Times are ticks of the Minecraft day (0 is 6:00).

- **Hours:** about a third of residents are early birds (up around 5:00, in bed by 19:30) and others night owls (up at 7:00, in bed at 22:00), depending on personality; farmers, fishermen, cooks, butchers and clerics are early birds, and tavern keepers and bards night owls. Everyone's times vary by up to twelve minutes, so a village doesn't move in lockstep.
- **An ordinary day:** wake, breakfast at home, work (8:00–15:00 with a lunch hour at 11:30, spent at the bell, at home or at the tavern), their hobby, catching up with the neighbors at the bell (16:30), supper at home (17:30), an evening at home or now and then at the tavern, then bed.
- **Jobs:** farmers and fishermen work 6:30–14:00; cooks keep the kitchen going 6:15–13:00 without a break; painters wait for good light (9:00–16:00); scholars work until 17:00; clerics start with morning prayers; the tavern keeper works 11:00–19:45; the bard practices in the morning and performs at the tavern 18:00–19:45; nitwits wake late, nap after lunch and end at the tavern. About half of all knights and archers keep the **night watch** (18:00–8:00, patrolling around the bell) and sleep until mid-afternoon.
- **Children** have breakfast, play, **lessons by the bell** (10:00–11:30), lunch at home, play again, supper at 17:00 and bed at 19:30.
- **Market Day:** every seventh day (the village week runs Moonday, Bellday, Hearthday, Wellday, Lanternday, Hayday, Market Day) nobody works except the cook; everyone goes to the market at the bell in the morning, spends the afternoon on hobbies and the evening at the tavern.

Each part of the day becomes a vanilla activity, so pathfinding, doors, beds, panic, raids and the bell keep working: bed and time at home (waking, meals, evenings, sheltering) use REST, but `SleepInBedRoutineMixin` keeps residents awake unless it is actually time to sleep (or nap); work and prayers use WORK; lunch at the bell, neighbors, the market and lessons use MEET; the tavern, hobbies and the night watch use IDLE, with `ResidentRoutines` walking residents to the tavern (the nearest tavern keeper's station), to a hobby spot picked each day (water for anglers, flowers or farmland for gardeners, a bench for carvers, open sky for stargazers, home for bakers and readers), or around the bell on patrol. Companions, guards in a fight, trading residents and residents with AI turned off follow their usual rules.

## Weather

`ResidentRoutines.weather` reads the sky where the resident lives: rain, a thunderstorm, snow in cold biomes, nothing in deserts, and "clearing" for a minute after rain stops.

- **Rain** sends residents who are outdoors home, or under the nearest roof if they have no bed, at a hurry and with a sweat bubble. Rain lovers (more often playful, adventurous and curious residents, and children) stay out instead. Indoor work goes on; farmers, shepherds, fishermen, masons and guards on duty keep working in ordinary rain.
- **Thunderstorms** send everyone in except guards on duty, who "stand guard in the storm". Children show a sweat bubble.
- **Snow** keeps the cold-averse at home by the fire while children and snow lovers play in it; work goes on.
- When the rain stops, some residents come out with a sparkle bubble.

The resident's part of the day is synced to clients (`villagefriends:routine`) and becomes the animation tag `routine:<part>`: work clips are three times as likely during working hours and hobby clips four times as likely during hobby time (`ROUTINE_BOOSTS` in `tools/animations/animations.py`). The conversation window's status line shows what they're doing and the time ("Catching up with neighbors · 16:45 · Market Day"), and each resident's Village Ledger page shows their hours and their day ("Early bird · Now: At work", "Today: 5:12 up · 5:27 breakfast · 6:30 work · ...").

## Workstations

All eleven workstations were redesigned as multi-part models with their own pixel art: a burlap training dummy with stitched eyes, a painted bullseye and an iron pot for a helmet; a straw archery boss with archery rings and two arrows stuck in it; a brick and cast-iron kitchen stove with a stew pot, a copper kettle, a towel and a chimney pipe, whose firebox glows when it's lit; a barrel on a cradle with an apple brand, a brass spigot and a mug of cider on top; a copper coffee urn on a spruce cabinet; an herb press with a screw, a turning bar, a vat of herbs and a bottle of tonic; an easel with a canvas that shows nine states; a brass music stand with sheet music and a candle; a sewing table with bolts of cloth, a runner, a spool and a pincushion; a sawmill bench with a round blade, a log and sawdust; and an archive cabinet of scrolls, ledgers and boxes with an open ledger and a candle. Wood and stone use vanilla textures so they sit naturally in villages.

| Station | For players | When its resident works there |
|---|---|---|
| Training Dummy (knight) | Strike it to see the damage of each hit and your combo; it isn't mined (sneak to pick it up) | The knight spars with it and gains a little guard experience (up to 15 a day) |
| Archery Target (archer) | Arrows score 1–10 by distance from the bullseye | The archer shoots blunt practice arrows at it and gains guard experience |
| Kitchen Stove (cook) | Cooks four raw foods at twice campfire speed; they pop out on top | The fire stays lit and there's a dish of the day: one helping of bread or stew per visitor per day |
| Drinks Barrel (tavern keeper) | Apples and berries press into cider; an Empty Coffee Mug becomes a **Mug of Cider** (food, short regeneration) | Restocked with four mugs |
| Tap Stand (tavern keeper) | Cocoa beans brew coffee; a mug becomes a Steaming Coffee Mug | Restocked with four mugs |
| Alchemical Press (apothecary) | Press flowers, berries, ferns or kelp (up to 12); three herbs and a glass bottle make an Herbal Tonic | Hurt residents nearby heal; hurt players get a few seconds of regeneration |
| Easel (painter) | A dye sketches the canvas; a second dye finishes one of seven paintings chosen by its color; take it off with an empty hand to get a painting; a paintbrush paints a finished canvas over | The painter paints a new picture over the day |
| Music Stand (bard) | Plays one of ten songs; Haste for a minute to players nearby, and nearby residents cheer; a held lute, bell, amethyst or bamboo changes the instrument | The bard performs |
| Sewing Table (tailor) | Wool unravels into three string; string mends leather, bows, crossbows, rods and elytra a quarter per length | The tailor mends the armor of guards nearby |
| Sawmill (carpenter) | Up to 16 logs a click, each into half again as many planks; a plank into three sticks | Leaves up to 16 sticks of offcuts to take |
| Archives (scholar) | Opens the village's ledger; a book becomes the **Chronicle of the village** | Players nearby study and gain experience (up to 30 a day) |

The stove and easel have block states (`lit`, `art`); everything else lives in the block entity. A resident's work effect runs each time vanilla's `WorkAtPoi` has them work at their station, roughly every half a minute. The custom professions also have their own work sounds now.

To change a model or texture, edit its design in `tools/workstations/workstations.py` or its art in `paint.py`, then run:

```text
python tools/workstations/workstations.py            # models, blockstates, item models, textures
python tools/workstations/workstations.py --check
python tools/workstations/workstations.py --preview  # build/previews/workstations.png and one image per model
python tools/workstations/workstations.py --boxes    # collision boxes to paste into VillageBlocks.java
```

One texel is always 1/16 block. Faces take vanilla's default UVs (shifted a block when an element pokes above it); tall faces give explicit UVs. Transparent pixels make cutout faces automatically, and `light_emission` makes the stove's fire glow. `tools/create_foundation_assets.py` still owns the other foundation blocks and skips the workstations.

## Dialogue

Every conversation line comes from the dialogue bank: **5,898 pieces of dialogue** written by hand: 4,861 lines in 411 pools, and 146 questions and offers with 441 answers (each a label and a reply). `Talk.pools` decides which pools a moment draws from and how likely each is:

| Topic | Draws from |
|---|---|
| The greeting | the time of day (7 periods), how well they know you (5 bands), the weather, what they're doing, their personality, Market Day, what you're holding, how you look |
| How's your day? | their personality (45 lines each), general chat, chat for strangers, friends or close friends, what they're doing, the weather, the time, the moon at night, Market Day and the village week, their hometown's biome, what you're holding, how you look, a golem, cat, wandering trader or children nearby, and answers you gave them before |
| Tell me about work | their job (35 lines each for all 25 jobs), how to use their workstation, whether they're at work or off duty, work in bad weather |
| Talk about adventures | their personality, rumors and stories, faraway places, night travel |
| Share a joke | 200 general jokes, their personality's and their job's |

Children have their own voice for every topic, the weather and their day. A line isn't repeated while it's among the last twelve that resident said to you; personality pack lines from `content.json`, village references, neighbor gossip and story callbacks still join in.

**Placeholders** fill lines from the world: `{name}`, `{player}`, `{village}`, `{job}`, `{hobby}`, `{love}`, `{friend}`, `{partner}`, `{rival}`, `{neighbor}`, `{time}`, `{day}`, `{weekday}`, `{market}`, `{moon}`, `{biome}` and `{item}`. A line whose placeholder can't be filled (no best friend yet, nothing in hand) is skipped.

**Questions.** About one "How's your day?" in four, a resident asks you something instead, and the reply bubbles become your answers. There are 121 questions: about you, would-you-rathers, opinions, little dilemmas, riddles with a right answer, and questions that fit their personality, their job, the weather or the time. Each is asked once; answering earns a little friendship, and many answers are remembered: they come back later in conversation ("You told me you love the rain. I thought of you all through the last storm.").

**Offers.** When the moment fits, a resident offers to help instead, at most once a day per offer: patching you up when you're hurt (healers, kind residents and good friends), food when you're hungry (cooks, farmers, butchers, fishermen, the tavern keeper), waiting out the rain or a storm together, torches at night, cooking the raw food you're holding, mending your damaged gear (smiths, tailors, leatherworkers), directions home, a fishing tip and a fish, a passage from a book for experience, a song, a cookie, a flower, an apple, a handful of seeds, a guard to walk you out at night, and, for very good friends, an emerald for luck. Accepting does it.

To write more, add lines under a `## pool.key` heading in `tools/dialogue/lines/`, or a question in `tools/dialogue/questions/`:

```text
? sunrise_sunset | when: morning
Q: Be honest with me. Are you a sunrise person or a sunset person?
- Sunrise, always :: Me too! The whole village goes pink for a minute. @likes:sunrise {points:1} [SPARKLE]
- Sunset, easily :: Then you'd love the view from the bell around six. @likes:sunset {points:1}
```

`?` asks once; `!` is a daily offer. `when:` lists tags that must all hold (`rain`, `night`, `market`, `hurt`, `hungry`, `wet`, `dark`, `damaged`, `held:<kind>`, `job:<job>`, `personality:<id>`, `routine:<part>`, `child`), `a|b` for either, `!tag` for not, and `level:N` for a friendship level. After a reply, `@flag` is remembered (write callbacks under `## remember.<flag with _ for :>`), `{effect}` does something (`heal`, `meal`, `shelter`, `torch`, `cook_held`, `mend_held`, `directions`, `fish`, `study`, `flower`, `apple`, `bread`, `cookie`, `seeds`, `emerald_tip`), `{points:N}` adds friendship and `[MOOD]` picks the speech bubble. Labels stay under 30 characters. Then run:

```text
python tools/dialogue/dialogue.py           # compile
python tools/dialogue/dialogue.py --check
python tools/dialogue/dialogue.py --stats   # counts by pool family
```

The compiler rejects duplicate lines, unknown placeholders and effects, long labels and malformed questions. A data pack can replace `data/villagefriends/villagefriends/dialogue.json`; `/reload` validates it and keeps the working bank if it's invalid.

## Verification

- `gradlew test` runs `RoutineTest` (hours, jobs, guards' watches, children, Market Day, rain, storms and snow), `DialogueBankTest` (the count, no duplicates, a pool for every personality, job, part of the day, weather, time, moon and home, fillable placeholders, remembered answers, sixty chats that barely repeat) and `TalkTest` (placeholders, periods and bands, which pools a moment uses, offers only when they fit, questions asked once).
- `gradlew runClientGameTest -Ptests=WorkstationGameTest` places and photographs every workstation, uses each one as a player, has a cook, painter, tavern keeper and knight work at theirs, follows a resident through midnight, a thunderstorm and clear skies, checks written dialogue on every topic and a remembered answer, and accepts an apothecary's offer to patch up a hurt player. Screenshots are named `workstations-*`.
