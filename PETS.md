# Residents' pets

Some residents long for a cat or a dog. In their free time they look for a stray, win them over, and from then on the two go everywhere together: the pet trots after them around the village, curls up beside their bed at night, keeps watch over them if they're knocked out, and every so often the two of them stop to play.

## Who keeps a pet

Whether a resident wants a pet, and which kind, is fixed by who they are (`PetKeeping.wish`): about two residents in five want one. Warmhearted, gentle and playful residents are the keenest; meticulous and reserved ones the least. Adventurous, protective and steadfast residents mostly want dogs; thoughtful, reserved, gentle and imaginative ones mostly want cats. Children can want pets too. Everyone else is happy without.

## Befriending a stray

During a free part of their day (a hobby, catching up with neighbors, market, evenings, lunch, play; or any daytime hour for the unemployed, nitwits and children), a resident who wants a pet looks for an untamed cat or wolf within 16 blocks. Village cats count. If there isn't one, a stray wanders into the village before long (a kitten or puppy now and then), never within sight of a player and never more than two at a time near a village. A stray who came for someone doesn't chase the village's sheep while it waits.

The resident walks up, crouches and holds out a fish or a bone. The stray creeps closer (a cat) or sits with its head tilted (a dog). Then either the stray accepts — hearts, a cheer, a name, a collar in a color that suits the resident, and a chat message to players nearby — or backs away in a puff of smoke, and the resident tries again a little later, with better odds each time. Players can still tame strays themselves first.

A resident's pet is tamed to them the vanilla way, so it gets a tame wolf's health, never despawns, defends its resident from monsters, and teleports to keep up. A resident's dog never bites a player, a neighbor or an iron golem.

## Following and resting

Pets trot to catch up whenever their resident gets more than seven blocks ahead, and teleport if they're more than twelve blocks away. While their resident sleeps, a cat curls up and a dog lies watch beside the bed. If their resident is knocked out, the pet stays beside them; a dog whines now and then.

## Playing together

Now and then (more often with playful pets and residents), a resident standing about in their free time stops to play with their pet. The resident acts out their part with a **pet** clip from the Village Life pack while the pet moves and strikes **tricks** (poses on the vanilla cat and wolf models). Each pet has a favorite game, which comes up most.

| Dogs | | Cats | |
|---|---|---|---|
| **Fetch** | The resident teases with a stick, throws it, watches the dog race off and bring it back in its mouth, takes it and pats the dog. Needs a few blocks of open, dry ground. | **String** | The resident dangles a bit of string; the cat bats at it, wiggles and pounces. |
| **Belly rubs** | The dog rolls onto its back, paws paddling, while the resident kneels and rubs; then it shakes off. | **Long strokes** | The cat lies down and purrs while the resident strokes it, then has a big stretch. |
| **Begging** | The dog sits up and begs while the resident holds a treat high, then catches it. | **Chin scratches** | The cat sits and leans into the scratch, purring. |
| **Shaking paws** | The dog sits and offers a paw to shake. | **Feather** | The cat chases a swishing feather in circles and pounces on it. |
| **Spinning** | The resident twirls a finger and the dog spins in a circle, then bounces happily. | **Treat time** | The resident offers a fish; the cat sniffs it, eats it and grooms a paw. |
| **Chase** | The resident tags the dog and runs; the dog chases them around. | **Weaving** | The cat weaves round the resident's ankles, tail up, while they watch fondly. |

Cats don't play in the rain. A game stops if either of them gets hurt, the resident is needed elsewhere (a trade, a player's outing, a raid) or they drift too far apart.

## The pet card

Right-click a resident's pet to open their card, in the same style as a resident's conversation window: the pet's portrait rising out of the dialogue box, their name on a ribbon, a line about them typing out, and a name-tag card with their owner (and the owner's trade and village), age, breed, nature, favorite game and treat, when they came home, health, and ten hearts of **fondness** for you. **Pat** them once a day for +6 fondness; **Give treat** (fish for cats, meat for dogs, from your main hand) heals them and, once a day, adds +10 fondness (+15 for their favorite). Sneak, a name tag or a lead still work the vanilla way. A resident's conversation card mentions their pet.

## When a resident or pet is gone

If a pet dies, their resident is sad and may adopt another stray later. If a resident dies for good, their pet becomes a stray again, keeping their name and remembering who they belonged to, and another resident may take them in. A resident who is turned into a zombie villager and cured keeps their pet.

## Files

| What | Where |
|---|---|
| Who wants a pet, names, natures, games, treats, ages, card lines | `pet/PetKeeping.java` (unit-tested in `ResidentPetsTest`) |
| The games and taming, step by step | `pet/PetPlays.java` |
| Stray arrivals, taming, playing, following, the card | `pet/VillagerPets.java` |
| The resident's part (24 `pet` clips) | `tools/animations/village_life/pets.py`, compiled into `village_life.json` |
| The pet's part (20 tricks) | `tools/pets/tricks.py`, compiled to `assets/villagefriends/pet_tricks/pets.json` |
| Posing cats and dogs | `client/PetPoser.java`, `WolfPoseMixin`, `FelinePoseMixin`; the fetch stick in `PetCarryLayer` |
| The card | `client/PetScreen.java` |

## Pet tricks

Tricks are client resources like resident clips: `assets/<namespace>/pet_tricks/*.json`, one file with a list of tricks keyed by species and id. A resource pack can replace the bundled file or add tricks; later files replace tricks with the same species and id.

```json
{"format": 1, "tricks": [
  {"id": "play_bow", "species": "dog", "length": 1.08, "loop": true, "blend": [0.25, 0.3],
   "tracks": {"root.rot": [[0, 14, 0, 0], [1.08, 14, 0, 0]], "right_front_leg.rot": [[0, -62, 0, 0], [1.08, -62, 0, 0]]}}
]}
```

Bones: `root`, `head`, `body`, `upper_body` (a grown dog's shoulders), `tail`, `tail_tip` (a cat's tail tip, which isn't attached to the rest of the tail), `right_front_leg`, `left_front_leg`, `right_hind_leg`, `left_hind_leg`. Tracks are `<bone>.rot` (degrees) or `<bone>.pos` (model pixels), keyed `[seconds, x, y, z]`, added to the pet's own pose (standing, sitting or lying as the game has it). Pitch + tips a bone down and back (a paw swings backward, the head looks down); pitch − raises a paw forward. The root turns the whole pet about the middle of its body, so it can roll onto its back or spin on the spot. Offsets are written for a grown pet and halved for kittens and puppies. Looping tricks repeat until the pet does something else; one-shot tricks fade out at their end.

```text
python tools/pets/tricks.py                    # compile tools/pets/tricks.py
python tools/pets/tricks.py --check            # validate and confirm the JSON is current
python tools/pets/tricks.py --list             # every trick
python tools/pets/preview.py sheet [--species cat] [--tricks bat,pounce] [--baby] [--frames 5] [--scale 9]
                                               # offline contact sheet on the vanilla models (textures read from the
                                               # Minecraft jar in the Gradle cache, never copied into the repository)
gradlew.bat runClientGameTest -Ptests=PetGameTest   # in-game checks and screenshots of each game
```

The resident's clips use the `pet` trigger with the tags `play:<phase>` and `pet:cat` or `pet:dog` (see [ANIMATION_PACKS.md](ANIMATION_PACKS.md)). A resident moving from one part of a game to the next cross-fades between clips.
