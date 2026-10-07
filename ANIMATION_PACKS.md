# Resident animation packs

Residents choose what to do from moment to moment. Standing residents fidget, practice their trade or hobby, chat with a neighbor beside them, greet a player who walks up, gesture while you talk with them, and react to jokes, gifts, trades, hearts, anger, fear and harm. Every one of those motions is a **clip** in an **animation pack**. The first pack, **Village Life**, ships with the mod.

Packs are client resources. A resource pack can add new packs, replace the bundled one, or switch individual clips off. Packs only describe motion; the director in `ResidentLife.java` decides when each clip plays. Nothing about animation is saved in worlds or sent to the server.

## Village Life (pack 1)

99 clips (90 distinct motions; a few serve two situations):

| Situation | Clips |
|---|---|
| Everyday idles | look around, shift weight, big stretch, yawn, scratch head, cross arms, hands on hips, rock on heels, hum a tune, dust off sleeves, roll neck, wipe brow, rub hands, kick a pebble, sneeze, pat pockets, shrug, side stretch, tap foot, watch the sky |
| One hobby per personality | knead dough (warmhearted), read a book (thoughtful), conduct a tune (playful), scout the horizon (adventurous), inspect a trinket (meticulous), tend the soil (steadfast), cast a line (reserved), frame the view (imaginative), whittle (pragmatic), stargaze (curious), sand a plank (protective), smell a flower (gentle) |
| Work for every profession | hammer at the anvil (smiths, mason, carpenter), hoe the rows (farmer), write notes (cartographer, librarian, scholar), pray (cleric), chop vegetables (butcher, cook), stir the pot (cook, apothecary, tavern keeper), pour a drink (tavern keeper), stitch cloth (tailor, leatherworker, shepherd), sight an arrow (fletcher, archer), stand guard (knight, archer), sword drill (knight), practice the draw (archer), twiddle thumbs (unemployed, nitwit), silly dance (nitwit, children) |
| Greetings | wave hello, bow politely, nod hello, salute (guards), wave excitedly (children) |
| Talking with you | explain, gesture with both hands, point to self, nod along, think it over, tilt head, count on fingers, shrug, chuckle, gasp |
| Chatting with a neighbor | tell a story, point somewhere, explain, gesture, count (speaking); listen politely, nod, chuckle, listen with arms folded, gasp (listening) |
| Reactions | belly laugh, giggle (a joke); cheer, hug the gift (a loved gift); bashful thanks, grateful nod (a gift); shake head, wag a finger (a refused gift or trade); clap, fist pump, cheer (happy sparkles); lovestruck sway (hearts); huff, shake a fist (angry clouds); nervous glances (raid sweat); flinch, stagger (harm) |
| Weather | hunch in the rain, catch raindrops, shake off the rain, shiver (snowy biomes) |
| Children | hop, twirl, play airplane, peekaboo, watch a bug, want to play tag |

## How the director chooses

Each resident is ticked on the client. When they have stood still for a second and their last clip has finished, they rest for a moment (shorter for lively personalities and children), then pick a clip for the situation:

| Trigger | When |
|---|---|
| `idle` | Standing around: everyday idles, work, hobbies, weather and children's play all compete by weight. |
| `chat_speak`, `chat_listen` | Another resident stands within about three blocks in front of them. Partners take turns speaking and listening every few seconds. |
| `greet` | A player who was away walks up within five and a half blocks in front of them (once a minute at most), or a conversation opens. The head turns to the player. |
| `talk` | The player has this resident's conversation window open. |
| `laugh`, `delighted`, `thanks`, `decline` | Conversation outcomes: a joke, a loved gift, an accepted gift, a declined gift. `decline` also plays when a resident refuses to trade. |
| `happy`, `love`, `angry`, `nervous` | Vanilla villager events: happy sparkles, hearts, angry clouds, raid sweat. |
| `hurt` | The resident takes damage. |

Reactions play on a second layer and briefly replace the current activity. While walking, reactions keep their upper body and leave the stride alone; activity clips fade out when a resident starts moving.

Clips are eligible by **tags** describing the resident and the moment:

| Tag | Meaning |
|---|---|
| `adult`, `child` | Age. |
| `job:<profession>` | `job:farmer`, `job:knight`, `job:none`, `job:nitwit`... Also `smith` for armorer/toolsmith/weaponsmith and `guard` for knight/archer. |
| `personality:<id>` | The resident's personality from the content pack (`warmhearted`, `playful`...). |
| `morning`, `day`, `evening`, `night` | Overworld time. |
| `rain`, `thunder`, `cold` | Rain falling on the resident, a thunderstorm, a snowy biome. |
| `holding`, `social` | Something in the main hand; a chat partner nearby. |

A resident never repeats their last two clips if anything else fits. About one resident in nine is left-handed and mirrors one-handed gestures.

## File format

Packs live at `assets/<namespace>/resident_animations/<pack>.json`. The bundled file is `assets/villagefriends/resident_animations/village_life.json`; a resource pack with a file at that path replaces it. A pack's clips are named `<pack>:<clip>` (`village_life:yawn`); packs from other namespaces are named `<namespace>.<file>`. Later packs replace clips with the same name. Use F3+T to reload. A pack that fails validation is skipped and named in the log; the others still load.

```json
{
  "format": 1,
  "name": "My Pack",
  "description": "Optional.",
  "disable": ["village_life:sneeze"],
  "clips": [
    {
      "id": "polite_wave",
      "name": "Polite wave",
      "trigger": "greet",
      "length": 2.0,
      "weight": 3,
      "require": ["adult", "personality:reserved|personality:gentle"],
      "avoid": ["rain"],
      "boost": {"morning": 2},
      "blend": [0.25, 0.35],
      "mirror": "hand",
      "items": "keep",
      "tracks": {
        "right_arm.rot": [[0, 0, 0, 0], [0.4, -20, 0, 120], [1.2, -20, 0, 130], [2.0, 0, 0, 0]],
        "head.rot": [[0, 0, 0, 0], [0.6, 10, 0, -6], [2.0, 0, 0, 0]],
        "eyes.lid": [[0, 0], [0.5, 0.3], [2.0, 0]]
      }
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `format` | Always `1`. |
| `disable` | Clip names from other packs to switch off. |
| `id` | Lowercase letters, digits and underscores. |
| `trigger` | One of the triggers above (default `idle`). |
| `length` | Seconds, up to 30. |
| `weight` | Relative chance against other eligible clips (default 1). |
| `require` | Every entry must match; `a|b` matches either tag. |
| `avoid` | Any matching tag rules the clip out. |
| `boost` | Weight multipliers for matching tags. |
| `blend` | Seconds to fade in and out (default 0.25, 0.35). |
| `mirror` | `hand` mirrors for left-handed residents (default), `free` also mirrors at random, `never` keeps it as written. |
| `items` | `keep` (default) leaves an arm that holds an item in its vanilla pose; `override` animates it anyway, so a smith's hammer swings. |

**Tracks** are named `<bone>.rot`, `<bone>.pos`, `eyes.lid` or `eyes.look`. Keys are `[seconds, x, y, z]` (`[seconds, value]` for `eyes.lid`, `[seconds, x, y]` for `eyes.look`) with strictly increasing times inside the clip. Values between keys follow smooth monotone curves: they never overshoot a key and hold still between equal keys. Start and end every track at zero so clips blend cleanly.

| Bone | Pivot |
|---|---|
| `head`, `body`, `right_arm`, `left_arm`, `right_leg`, `left_leg` | Their own joints. |
| `waist` | Bends the body, head and both arms together at the hips, so bows keep the feet planted. Rotation only. |
| `root` | Turns the whole resident about the feet; `root.pos` lifts or lowers them (a hop). |

Rotations are degrees added to the live pose (vanilla look direction, gait and breathing), in Minecraft's model space: a negative `x` raises a limb forward (−90 points it ahead, −180 straight up), while a positive `x` tips the head down and bends the waist forward. For the right arm and leg, positive `z` lifts the limb outward; for the left side, negative `z` does. Once an arm is raised above the shoulder, `z` tips it the other way, so a V overhead is easiest as a side raise (`[x≈-10, 0, ±160]`). Positions are model pixels (`y` negative is up, `z` negative is forward), written for an adult; children scale them to their size. `eyes.lid` closes the eyes from 0 to 1 on top of natural blinking; `eyes.look` moves the irises (`x` positive toward the resident's left, `y` positive down), kept inside the eye whites.

## Authoring Village Life

The bundled pack is written in Python with `tools/animations/kit.py`, which uses mirror-friendly conventions (both arms lift outward with positive roll) and converts to model space. Never hand-edit the compiled JSON.

```text
python tools/animations/animations.py             # compile tools/animations/village_life/*.py
python tools/animations/animations.py --check     # validate and confirm the JSON is current
python tools/animations/animations.py --list      # every clip, its trigger and length
python tools/animations/preview.py sheet --clips yawn,cheer --frames 6 --scale 6   # offline poses
gradlew.bat runClientGameTest -PanimationPack     # in-game checks and a still of every clip
gradlew.bat runClientGameTest -PanimationVideo    # 30 fps showcase frames (development only)
python tools/animations/film.py                   # titles, crossfades and an H.264 MP4
```

`-PanimationVideo` takes `-PfilmScenes=gallery,village` and `-PfilmStride=15` (every fifteenth frame, for checking composition). It builds a procedural village on a superflat world, stages residents around the fountain and steps a frozen world one tick per frame, rendering between ticks, so the footage is smooth and repeatable.
