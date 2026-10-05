package dev.villagefriends.outfit;

import java.util.List;
import java.util.Objects;

/**
 * One dressed resident: a hairstyle with natural hair color, a top and a bottom, all resolved
 * through a single palette. The template records which profession outfit inspired it; the bottom
 * may differ from the template's when the factory mixes compatible pieces.
 */
public final class Outfit {
    private final Gender gender;
    private final Profession profession;
    private final ColorPalette palette;
    private final Garment hair, top, bottom;
    private final HairColor hairColor;
    private final Wardrobe.OutfitTemplate template;

    public Outfit(Gender gender, Profession profession, ColorPalette palette, Garment hair, HairColor hairColor,
                  Garment top, Garment bottom, Wardrobe.OutfitTemplate template) {
        this.gender = Objects.requireNonNull(gender, "gender");
        this.profession = Objects.requireNonNull(profession, "profession");
        this.palette = Objects.requireNonNull(palette, "palette");
        this.hair = Objects.requireNonNull(hair, "hair");
        this.hairColor = Objects.requireNonNull(hairColor, "hair color");
        this.top = Objects.requireNonNull(top, "top");
        this.bottom = Objects.requireNonNull(bottom, "bottom");
        this.template = Objects.requireNonNull(template, "template");
        if (hair.kind() != Garment.Kind.HAIR || !Wardrobe.compatible(top, bottom)) throw new IllegalArgumentException("Incompatible outfit");
    }

    public Gender gender() { return gender; }
    public Profession profession() { return profession; }
    public ColorPalette palette() { return palette; }
    public Garment hair() { return hair; }
    public HairColor hairColor() { return hairColor; }
    public Garment top() { return top; }
    public Garment bottom() { return bottom; }
    public Wardrobe.OutfitTemplate template() { return template; }

    /** Skin-layer painting order: a tucked top goes under the bottom's waistband; hair last. */
    public List<Garment> layers() { return top.tucked() ? List.of(top, bottom, hair) : List.of(bottom, top, hair); }
    public List<Garment> garments() { return List.of(hair, top, bottom); }
    /** The top's own belt or long hem hides the bottom's waist pieces. */
    public boolean shows(Garment garment, Piece piece) {
        return !(garment == bottom && top.coversWaist() && piece.id().startsWith("waist"));
    }
    public Outfit recolor(PaletteID id) { return new Outfit(gender, profession, MasterPalettes.get(id), hair, hairColor, top, bottom, template); }
    public Outfit withBottom(Garment other) { return new Outfit(gender, profession, palette, hair, hairColor, top, other, template); }
    /** Stable texture-cache identity (complexion is added by the renderer). */
    public String key() { return palette.id() + "_" + hairColor.id() + "_" + hair.id() + "_" + top.id() + "_" + bottom.id(); }
}
