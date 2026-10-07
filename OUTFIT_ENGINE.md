# Wardrobe and outfit engine

Residents dress like characters from a Sims-style wardrobe with a men's set and a women's set. Men pick from 80 hairstyles, 120 tops and 120 bottoms; women from 50 hairstyles, 60 tops and 60 bottoms; non-binary residents from both. Every outfit is colored by one of 10 master palettes, and hair by one of 10 natural hair colors.

The first ten of each kind are the original set, drawn from the user's male reference. Version 2.8 added twenty casual-medieval tops and bottoms (tunics, smocks, jerkins, hoods, cloaks, braies, trews, kilts, chausses, clogs and boots) and twenty anime-inspired hairstyles. Version 2.11 made those ninety pieces the men's set and added:

- **Men:** fifty hairstyles (crops, curls, coils, locs, cornrows, braids, buns, warrior tails, long manes, a tonsure and balding elder styles); seventy casual-medieval tops and bottoms for trades, clergy, nobles, soldiers, regions and festivals; and a twenty-piece *supreme casual* line of plain tees, tunics, polos, shirts, chinos, slacks and jeans.
- **Women:** the first women's wardrobe: fifty hairstyles (long, braided, tailed, bunned, bobbed, curly, coily and locked) and sixty tops and bottoms such as kirtles, bodices, chemises, overgowns, aprons, skirts, breeches and armor, with an outfit for every profession.

The hairstyles use clean cel shading, a sheen ring and tapered pointed locks, but stay grounded: no gravity-defying spikes. The supreme casual line is the one deliberate exception to the medieval cut; everything else avoids modern clothing. The previous voxel/role-mask wardrobe and its registries were removed and replaced at the user's request. To add or change clothing, read [WARDROBE_EDITING.md](WARDROBE_EDITING.md).

## Pieces

Each hairstyle, top and bottom is one PNG and one JSON file under `assets/villagefriends/wardrobe/{hair,tops,bottoms}/`. Both are compiled from one Python module per piece in `tools/wardrobe/`.

- **Skin layer:** the top 64×64 of the PNG is painted in the standard player-skin layout. The base layer is the body; the hat, jacket, sleeve and pants overlays give clothing and hair half-pixel depth.
- **3D pieces:** the rows below the skin layer hold box-UV nets for the piece's cuboids, such as pauldrons, collars, coat skirts, hoods, cuffs, pouches and hair locks. Each cuboid is attached to a body bone with a pivot, a rotation in degrees and an optional inflation.
- **Motion:** the `flap_front` and `flap_back` motions follow the leading or trailing leg so coats and aprons never clip through a stride. `sway` swings ponytails, tassels and sash tails while the resident walks.

## Palette lock

The PNGs contain no clothing color. Every opaque pixel is a *key color*: a role (primary 60%, secondary 30%, accent 10%, the materials leather, metal, ink and denim, or natural hair) plus one of five shades (deep, shadow, base, light, highlight).

- **Palettes:** `palettes.json` stores the ten master palettes as five-shade ramps. Shadows shift cooler and highlights warmer, so pixel-art shading stays within the palette. Each palette has its own tone of every material, including a denim wash, so jeans read as denim while still matching the outfit.
- **Plain colorways:** a plain garment takes its color from the role it is painted in. The supreme casual tees and tunics use one cut in five roles each, so they come out as five differently colored shirts in every palette.
- **One palette per outfit:** each `Outfit` owns a single palette. Hair keys resolve through the natural `HairColor` ramp instead.
- **Shadow keys:** two translucent keys (`X1`/`X2`) darken whatever lies beneath them, such as hairline shadows or a tucked shirt's fold.

## Mix and match

The wardrobe is Sims-style: within a resident's set, any top pairs with any bottom unless a rule forbids it.

- **Tag rules:** armor tops `require` sturdy legwear, plated legs require a martial or rugged top, and fancy hose, kilts and sandals `reject` armor.
- **Locked sets:** a few outfits only work as one piece. Their top and bottom name each other (`locked_to`) and are always worn together, never mixed. The men's set has 19 (monk, friar, herald, jester, crusader, morris dancer, green man and others); the women's has 8 (court gown, nun, abbess, sun priestess, coin dancer, May dancer, houppelande and heraldic gown).
- **Coverage:** every free top mixes with at least seven free bottoms of its set. 9,849 of the men's 10,201 free pairs and 2,665 of the women's 2,704 are allowed.

`Wardrobe.compatible` and `tools/wardrobe/wardrobe.py` apply the same rule.

Skin layers stack as: body, then the bottom, then the top, then hair. A `tucked` top (shirts) goes under the bottom instead, so waistbands and suspenders show over it. A top that `coversWaist` (its own belt, sash or long hem) hides the bottom's 3D pieces whose ids start with `waist`.

## Professions

Outfit templates (a top plus its matching bottom) live in one file per set, `tools/wardrobe/outfits/male.json` and `female.json`. The compiler merges them into `catalog.json`. Every top is in at least one template, and every profession has templates for both sets. `OutfitFactory.assembleOutfit` works in this order:

1. Everything comes from the resident's own set: men's, women's, or both for non-binary residents.
2. Hair and hair color come from the resident's seed alone, so a new job never changes them.
3. The profession's preferred template for that set is chosen 30% of the time; otherwise one of its alternatives is used.
4. The template's bottom is kept 50% of the time; otherwise a random compatible bottom from the set is used. A locked set is always worn whole.

The men's original templates are listed below. Bold professions prefer the template; the others use it as an alternative. The 90 newer men's templates (`m_` ids) and the 60 women's templates (`f_` ids) follow the same pattern in their files. Each women's profession prefers its own outfit, for example the Knight's lady-knight armor, the Cleric's nun's habit and the Farmer's farm wife.

| Template | Top | Bottom | Professions |
|---|---|---|---|
| Knight-Errant | Squire's Brigandine | Plated Greaves | **Knight**, **Guard**, Armorer, Weaponsmith |
| Trailblazer | Trailblazer Vest | Trail Breeches | **Cartographer**, **Adventurer**, unemployed, Leatherworker |
| Arcanist | Arcanist Longcoat | Scholar's Slacks | **Librarian**, **Scholar**, **Mage**, Cartographer, Apothecary |
| Farmhand | Farmhand Flannel | Patched Workpants | **Farmer**, unemployed, Mason, Shepherd, Carpenter |
| Merchant | Merchant's Waistcoat | Pinstripe Trousers | **Tailor**, **Merchant**, Librarian, Tavern Keeper, Painter |
| Mariner | Mariner's Knit | Rolled Canvas | **Fisherman**, unemployed |
| Smith | Smith's Apron | Heavy Work Trousers | **Armorer**, **Butcher**, **Leatherworker**, **Mason**, **Toolsmith**, **Weaponsmith**, Cook, Carpenter |
| Ranger | Ranger's Hood | Wrapped Leggings | **Fletcher**, **Archer**, Adventurer, Guard |
| Minstrel | Minstrel's Doublet | Minstrel Hose | **Nitwit**, **Painter**, **Bard**, Tailor |
| Pilgrim | Pilgrim's Tabard | Wanderer's Pantaloons | **Cleric**, Apothecary, Scholar |
| Villager | Belted Linen Tunic | Drawstring Trousers | **unemployed**, Nitwit, Butcher, Farmer, Fisherman |
| Goatherd | Drawstring Smock | Knee Braies & Stockings | unemployed, Nitwit, Farmer, Shepherd |
| Wayfarer | Clasped Half-Cloak | Tall Riding Boots | unemployed, Cartographer, Adventurer |
| Militia | Quilted Arming Jacket | Buttoned Gaiters | Armorer, Mason, Weaponsmith, Knight, Guard |
| Hunter | Laced Leather Jerkin | Leather Chaps | Fletcher, Leatherworker, Archer, Adventurer |
| Townsman | Liripipe Hood | Cross-Gartered Hose | Nitwit, Bard, Merchant |
| Burgher | Fur-Trimmed Houppelande | Woolen Chausses | Cleric, Tavern Keeper, Tailor, Merchant |
| Gallant | Buttoned Cotehardie | Belted Hose & Dagger | Knight, Tailor |
| Shepherd | Sheepskin Vest | Sheepskin Leg Wraps | **Shepherd** |
| Highlander | Wrapped Wool Shawl | Belted Wool Kilt | unemployed |
| Herbalist | Herbalist's Bandolier | Summer Trousers & Sandals | **Apothecary** |
| Innkeeper | Tavern Shirt & Half-Apron | Wool Trousers & Clogs | **Tavern Keeper**, Butcher, Cook |
| Northerner | Fur-Collared Coat | Fur-Topped Winter Boots | unemployed, Fisherman, Adventurer, Guard |
| Drover | Hooded Wool Poncho | Tartan Trews | unemployed, Fisherman, Shepherd |
| Yeoman | Layered Overtunic | Knee Breeches & Buckle Shoes | unemployed |
| Reveler | Embroidered Festival Vest | Striped Stockings & Breeches | unemployed, Nitwit, Painter, Bard |
| Woodsman | Woodsman's Wrap Jacket | Side-Laced Leather Trousers | **Carpenter**, Fletcher, Toolsmith, Archer |
| Baker | Baker's Floury Smock | Quilted Trousers | **Cook** |
| Gardener | Satchel & Overshirt | Pouch-Belt Trousers | Farmer |
| Student | Student's Open Gown | Embroidered Hem Trousers | Cartographer, Cleric, Librarian, Painter, Scholar, Mage |

Unknown or modded professions dress like the unemployed.

```java
Outfit outfit = OutfitFactory.assembleOutfit(Gender.MALE, Profession.MERCHANT, PaletteID.ROYAL_VELVET, 81L);
Outfit recolored = outfit.recolor(PaletteID.SAGE_AND_TERRACOTTA);
```

## Rendering

- **Model:** `ResidentModel` is the player mesh with its overlays and the Living Eyes parts, and nothing else.
- **Pieces:** `WardrobeLayer` bakes every garment's 3D pieces once as plain cubes. Each frame it places only the worn hair's, top's and bottom's pieces on their posed bones, so the frame cost does not grow with the wardrobe. With 490 hairstyles, tops and bottoms (about 4,400 pieces), the focused wardrobe test measured about 8 µs to pose a resident. Before, when every piece lived in the model, it measured 67 µs, and that was paid twice per frame.
- **Atlas:** `OutfitAtlas` lays out a 256×512 texture with the player skin at the origin, the face-detail swatches at (64..67, 0), and one 64-pixel-wide slot per kind for piece nets: hair at x 64 below the swatches, tops at x 128 and bottoms at x 192. An outfit wears one garment of each kind, so all garments of a kind share its slot and the wardrobe grows without growing the texture.
- **Baking:** `ResidentSkins` bakes one texture per complexion and outfit on a cache miss. It resolves key colors through the palette, applies the layering rules and copies the piece nets into their blocks. Animation allocates no textures.
- **Reload:** wardrobe PNGs reload with resource packs, so a pack can repaint any piece in key colors.
- **Armor:** a helmet hides the hair layer and hair pieces; chest and leg armor hide the matching garment pieces.
- **Eyes:** the Living Eyes UVs and face swatches are unchanged. Hair never paints the eye row, and the compiler rejects fringes that would hang over the eyes, nose or mouth.

## Recipes and genders

Recipes keep the `outfitN:complexion:GENDER:PALETTE_ID:seed` format. Saved residents keep their complexion, gender, palette, seed, identity and history, and are redressed from the expanded wardrobe: women now wear the women's set.

Each garment declares its set (`male`, `female` or `unisex`). `Wardrobe.hair/tops/bottoms(gender)` and `Wardrobe.templates(job, gender)` return what a resident of that gender wears. A gender without pieces of its own, or a job with no outfit for it, falls back gracefully.

## Verification

```text
python tools/wardrobe/wardrobe.py --check
gradlew.bat test
gradlew.bat runClientGameTest -PoutfitsOnly
gradlew.bat runClientGameTest -PhairFacesOnly
gradlew.bat runClientGameTest -PresidentSample
```

The focused Minecraft run checks palette lock on every baked texel, profession dressing for both sets, armor hiding and reload, and logs what posing the shared model costs. It also captures these screenshots in `build/run/clientGameTest/screenshots/`:

- every outfit template, ten per page, from the front, from the back and mid-stride
- every hairstyle, ten per page, from the front and back
- two mix-and-match galleries per set
- one outfit across all ten palettes
- an in-world scene for each page of outfits

`-PresidentSample` is a development sample rather than a regression test. It dresses five random men and five random women exactly as a new village would, with fresh recipes and real professions. It saves an in-world shot plus labelled front and back close-ups of each group, and logs every resident's pieces. Pass `-PsampleSeed=<n>` to repeat a draw.
