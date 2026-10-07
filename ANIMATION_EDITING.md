# Resident movement, animation packs and eyes

Walking, idling, gestures and facial presentation live in the resident renderer. They do not change AI, hitboxes, movement speed, professions or saved appearances. Two layers make residents feel alive:

1. **Always-on motion** (`ResidentAnimation.java`): individual gaits, breathing, a slow weight shift from hip to hip, a head that keeps drifting between the AI's look targets, a forward lean when hurrying, blinking and glances.
2. **Animation packs** (`ResidentLife.java`, `ResidentPoser.java`): authored clips the resident chooses for themselves: idles, work, hobbies, chats, greetings and reactions. Read [ANIMATION_PACKS.md](ANIMATION_PACKS.md) for the clip list, the director's rules and the pack format.

## Gaits

`src/main/java/dev/villagefriends/ResidentMotion.java` defines six gait styles. A resident's UUID selects its gait and small cadence/timing differences, so changing jobs or reloading a world keeps the same movement identity. Gaits are independent of complexion and clothing. `ResidentAnimation.java` applies these parameters to both `ResidentModel` and `ResidentArmorModel`, preventing armor from walking out of alignment.

Keep the walk itself small: gait sway is under two degrees; torso twist is about 1.5 degrees; the strongest step lift is less than one model pixel. Idle feet stay planted (the weight shift only rolls the hips and legs sideways). Active item-use, attacks, seats, water, airborne, crouching, sleeping and death poses retain their vanilla body animation. Children use the existing baby transformer and slightly quicker, shorter strides.

## Animation packs

`ResidentLife` is a client-side director per resident. It runs on client ticks (and holds still when the world is frozen with `/tick freeze`), picks clips with `AnimationLibrary.pick` and fills two layers of the render state each frame: an activity (idle, work, chat, talk) and a reaction (greet, laugh, gift, hurt...). `ResidentPoser` then adds the sampled clips to the live pose in this order: limb and head rotations, the waist (which bends the body, head and arms together around the hips), then the root (which pivots the whole resident about the feet). Both the resident and armor models call the same code, so armor never separates from a pose. An arm holding an item keeps its vanilla pose unless the clip says otherwise; while walking, reactions leave the stride alone.

Rules worth keeping when editing clips or the poser:

- Clips start and end at rest; reactions blend in quickly, activities fade out when a resident starts walking.
- Positions are written in adult pixels and scaled for children.
- Posing allocates nothing per frame and never touches textures.
- The resident's personality reaches the client through the synced `villagefriends:temperament` attachment so body language matches the Journal; the conversation window's portrait plays the same clips as the resident in the world.
- Conversation outcomes are cued from `FriendshipScreen` (joke, gift accepted/loved/declined); vanilla villager events (hearts, angry clouds, happy sparkles, raid sweat) arrive through `VillagerEventMixin`.

## Eyes and face

Every resident has one of two pixel-art eye styles for life, picked from their UUID's motion seed (`FaceDetails.eyeStyle`), about half each:

- **Starlit:** three rows tall. A lash line on face row 3; a tinted white beside a dark pupil on row 4; a white glint beside the iris on row 5.
- **Soft Glint:** two rows tall and lower. A lash line on row 4 over the glint and iris on row 5.

The iris sits in the inner column and the white on the outer one, so residents look at you. `ResidentModel.java` draws each feature as a plane in front of the face and behind the hair. The bottom white and the iris still sample the resident's own face row: whites at `(9,12)` and `(14,12)`, irises at `(10,12)` and `(13,12)`, lids at `(12,12)`. `ResidentSkins` bakes the other colors from them into swatches at `(64..71, 0)`: brow and lash from the hair color, a neck shade, the Starlit upper white tinted by the iris, the pupil, two lip tones and a blush. Resource packs that recolor the eye row recolor the whole eye.

Faces are young and clean: no nose, eye bags or chin shadow. Masculine faces have straight, fuller half-pixel brows and a small neutral mouth. Feminine faces add a lash wing at the outer corner (below a Starlit lash, flicking up from a Soft Glint lash), finer arched brows, rosy lips and blush. Women always wear the feminine details, men never, and non-binary residents get one or the other from their seed (`FaceDetails.feminine`).

To blink, the lash line sweeps down over the eye and thins slightly, and a skin lid follows it. Closed, the lash lies along the bottom of the eye and a feminine wing joins its outer end. Glances slide the iris and Starlit pupil by up to 0.28 px across and 0.09 px up or down, trimmed to the eye's edges so they never cross into skin. `FaceDetails` keeps the geometry (`eyeTop`, `lashBottom`, `wingTop`, `browTop`) in one place, and the unit and game tests use the same functions.

Blink timing comes from `ResidentMotion.blink`: about 0.2 seconds per blink, an individual interval of roughly five to eight seconds, varied timing within each cycle and occasional double blinks. There are no random draws, timer allocations, extra skin images or texture uploads per frame. Sleeping and dying residents have closed eyes. Clips can squint or close the eyes (`eyes.lid`, combined with blinking) and redirect the gaze (`eyes.look`), always inside the eye. `ResidentRenderer` supplies small pupil offsets toward the camera within six blocks and a front-facing cone; while greeting or talking, the head also turns toward the player.

## Verification

Build with `build.ps1`. Run focused native verification with the existing Java 25 environment:

```text
gradlew.bat runClientGameTest -PanimationsOnly
gradlew.bat runClientGameTest -PanimationPack
```

`-PanimationsOnly` renders the six walking styles at two sample moments, a close eye gallery and the actual conversation portrait, and exercises pathfinding-driven walking, armor alignment, special poses, children, helmets, texture-cache behavior and reload. `-PanimationPack` checks every clip's armor parity and planted feet, held items, mirroring, eyes and children, then drives real residents through idles, a neighbor chat, a greeting, a conversation (talking, a joke, a loved and a disliked gift), vanilla events, harm, a refused trade and a frozen world, and captures a still of every clip. Preview screens and test classes stay outside the release JAR.
