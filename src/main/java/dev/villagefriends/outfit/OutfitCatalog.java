package dev.villagefriends.outfit;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import static dev.villagefriends.outfit.BodyPart.*;
import static dev.villagefriends.outfit.ColorRole.*;
import static dev.villagefriends.outfit.LayerSlot.*;
import static dev.villagefriends.outfit.OutfitStyle.*;

/** Initial volumetric silhouettes; all garment materials are role masks. */
public final class OutfitCatalog {
    private static final Set<Gender> ALL = Set.of(Gender.values());
    public static final List<TopGarment> TOPS = List.of(
        top("hearth_tunic", RELAXED, 11, false, false),
        top("layered_tunic", RELAXED, 13, false, true),
        top("canvas_vest", WORKWEAR, 11, true, false),
        top("work_smock", WORKWEAR, 14, false, true),
        top("tweed_waistcoat", TAILORED, 11, true, true),
        top("merchant_coat", TAILORED, 16, false, true),
        top("scholar_robe", ROBES, 19, false, true),
        top("empire_dress", ROBES, 18, true, true),
        top("traveler_coat", TRAVELER, 15, false, true),
        top("mantled_jacket", TRAVELER, 12, true, true)
    );
    public static final List<BottomGarment> BOTTOMS = List.of(
        bottom("linen_trousers", Set.of(RELAXED, WORKWEAR), false, 12),
        bottom("tailored_trousers", Set.of(TAILORED, ROBES), false, 12),
        bottom("travel_breeches", Set.of(TRAVELER, WORKWEAR), false, 10),
        bottom("high_waist_skirt", Set.of(RELAXED, TAILORED), true, 11),
        bottom("pleated_skirt", Set.of(ROBES, TAILORED), true, 12),
        bottom("split_travel_skirt", Set.of(TRAVELER, WORKWEAR), true, 10)
    );
    public static final List<HairModel> HAIR = java.util.stream.IntStream.range(0, 10).mapToObj(OutfitCatalog::hair).toList();
    public static final List<Integer> HAIR_COLORS = List.of(0x342A26, 0x594134, 0x846344, 0xBBA16F,
        0xA66B47, 0x3B3737, 0x8A8580, 0xC3BEB1);
    public static final List<HairModel> ALL_HAIR = java.util.stream.Stream.concat(HAIR.stream(),MaleHairRegistry.MODELS.stream()).toList();
    public static final List<TopGarment> ALL_TOPS = java.util.stream.Stream.concat(TOPS.stream(),MaleTopRegistry.MODELS.stream()).toList();
    public static final List<BottomGarment> ALL_BOTTOMS = java.util.stream.Stream.concat(BOTTOMS.stream(),MaleBottomRegistry.MODELS.stream()).toList();
    public static List<HairModel> hair(Gender gender) { return gender==Gender.MALE?MaleHairRegistry.MODELS:HAIR; }
    public static List<TopGarment> tops(Gender gender) { return gender==Gender.MALE?MaleTopRegistry.MODELS:TOPS; }
    public static List<BottomGarment> bottoms(Gender gender) { return gender==Gender.MALE?MaleBottomRegistry.MODELS:BOTTOMS; }

    private static VoxelBox box(String id, BodyPart bone, int layer, float x, float y, float z,
                                float w, float h, float d) {
        return new VoxelBox(id, bone, layer, x, y, z, w, h, d, .025F);
    }
    private static MaskedVoxel cloth(String id, BodyPart bone, int layer, ColorRole role,
                                     float x, float y, float z, float w, float h, float d) {
        return new MaskedVoxel(box(id, bone, layer, x, y, z, w, h, d), RoleMask.solid(role));
    }
    private static ClothingLayer layer(String id, LayerSlot slot, MaskedVoxel... boxes) {
        return new ClothingLayer(id, slot, List.of(boxes));
    }

    private static TopGarment top(String id, OutfitStyle style, int length, boolean open, boolean collar) {
        var layers = new ArrayList<ClothingLayer>();
        layers.add(layer(id + "_shirt", UNDERLAYER,
            cloth("shirt", TORSO, 0, ROLE_SECONDARY, -4.05F, 1, -2.05F, 8.1F, 10, 4.1F),
            cloth("left_sleeve", LEFT_ARM, 0, ROLE_SECONDARY, -1.05F, -1.95F, -2.05F, 4.1F, 10, 4.1F),
            cloth("right_sleeve", RIGHT_ARM, 0, ROLE_SECONDARY, -3.05F, -1.95F, -2.05F, 4.1F, 10, 4.1F)));
        var outer = new ArrayList<MaskedVoxel>();
        outer.add(cloth("back", TORSO, 1, ROLE_PRIMARY, -4.2F, .4F, 2.05F, 8.4F, length, .35F));
        for (int side : new int[]{-1, 1}) {
            outer.add(cloth(side < 0 ? "front_left" : "front_right", TORSO, 1, ROLE_PRIMARY,
                side < 0 ? -4.2F : open ? 1.2F : 0, .4F, -2.4F, open ? 3 : 4.2F, length, .35F));
            outer.add(cloth(side < 0 ? "side_left" : "side_right", TORSO, 1, ROLE_PRIMARY,
                side < 0 ? -4.2F : 3.85F, .4F, -2.05F, .35F, length, 4.1F));
        }
        layers.add(new ClothingLayer(id + "_outer", OUTERWEAR, outer));
        var trim = new ArrayList<MaskedVoxel>();
        trim.add(cloth("belt", TORSO, 2, ROLE_ACCENT, -4.3F, 8.6F, -2.5F, 8.6F, .7F, .3F));
        trim.add(cloth("hem", TORSO, 2, ROLE_ACCENT, -4.3F, length - .3F, -2.5F, 8.6F, .55F, .3F));
        if (collar) for (int side : new int[]{-1, 1}) trim.add(cloth(side < 0 ? "lapel_left" : "lapel_right",
            TORSO, 2, ROLE_ACCENT, side < 0 ? -2 : .75F, .2F, -2.55F, 1.25F, 3.5F, .3F));
        layers.add(new ClothingLayer(id + "_trim", TRIM, trim));
        layers.add(layer(id + "_hardware", HARDWARE,
            cloth("buckle", TORSO, 3, ROLE_HARDWARE, -.55F, 8.5F, -2.75F, 1.1F, .95F, .3F),
            cloth("button", TORSO, 3, ROLE_HARDWARE, -.2F, 4.2F, -2.7F, .4F, .4F, .25F)));
        return new TopGarment(id, ALL, style, layers);
    }

    private static BottomGarment bottom(String id, Set<OutfitStyle> styles, boolean skirt, int length) {
        var shapes = new ArrayList<MaskedVoxel>();
        if (skirt) {
            shapes.add(cloth("front", TORSO, 1, ROLE_SECONDARY, -4.4F, 11.6F, -2.6F, 8.8F, length, .5F));
            shapes.add(cloth("back", TORSO, 1, ROLE_SECONDARY, -4.4F, 11.6F, 2.1F, 8.8F, length, .5F));
            for (int side : new int[]{-1, 1}) shapes.add(cloth(side < 0 ? "side_left" : "side_right", TORSO, 1,
                ROLE_SECONDARY, side < 0 ? -4.4F : 3.9F, 11.6F, -2.1F, .5F, length, 4.2F));
        } else {
            for (var bone : List.of(LEFT_LEG, RIGHT_LEG)) shapes.add(cloth(bone == LEFT_LEG ? "left_leg" : "right_leg",
                bone, 0, ROLE_SECONDARY, -2.05F, 0, -2.05F, 4.1F, length, 4.1F));
        }
        return new BottomGarment(id, ALL, styles, List.of(new ClothingLayer(id + "_fabric", BOTTOM, shapes),
            layer(id + "_trim", TRIM, cloth("waist", TORSO, 2, ROLE_ACCENT, -4.35F, 11.35F, -2.65F, 8.7F, .55F, .3F))));
    }

    private static HairModel hair(int variant) {
        String id = List.of("layered_crop", "tousled_quiff", "rounded_curls", "wavy_bob", "loose_waves",
            "high_bun", "twin_braids", "side_braid", "swept_fringe", "braided_crown").get(variant);
        var cubes = new ArrayList<VoxelBox>();
        // A hollow scalp shell keeps the face unobstructed; every part has nonzero depth.
        cubes.add(box("cap", HEAD, 0, -4.1F, -8.25F, -4.1F, 8.2F, 1.2F, 8.2F));
        cubes.add(box("back", HEAD, 0, -4.15F, -7.1F, 3.6F, 8.3F, 5.2F, .65F));
        for (int side : new int[]{-1, 1}) cubes.add(box(side < 0 ? "left" : "right", HEAD, 1,
            side < 0 ? -4.4F : 3.7F, -7.3F, -3.6F, .7F, 4.2F, 7.8F));
        for (int i = 0; i < 4; i++) cubes.add(box("lock_" + i, HEAD, 1,
            -4.1F + i * 2, -8.55F - (i + variant) % 3 * .15F, -4.4F + (i % 2) * .25F,
            2.05F, 1.25F + (i + variant) % 2 * .3F, 1.1F));
        if (variant == 1 || variant == 8) cubes.add(box("quiff", HEAD, 2, -2.8F, -9.3F, -3.8F, 5.2F, 1.3F, 2.4F));
        if (variant == 2) for (int i = 0; i < 4; i++) cubes.add(box("curl_" + i, HEAD, 2,
            -4.5F + i * 2.3F, -8.7F, -3.8F, 1.9F, 1.8F, 2));
        if (variant == 3 || variant == 4) cubes.add(box("waves", HEAD, 1, -4.3F, -2.5F, 3.55F, 8.6F, variant == 4 ? 7 : 2, .9F));
        if (variant == 5) cubes.add(box("bun", HEAD, 2, -1.8F, -7.8F, 4.05F, 3.6F, 3.4F, 2.8F));
        if (variant == 6 || variant == 7) for (int side : variant == 7 ? new int[]{1} : new int[]{-1, 1})
            for (int i = 0; i < 5; i++) cubes.add(box("braid_" + (side < 0 ? "left_" : "right_") + i,
                HEAD, 2, side < 0 ? -4.7F : 3.35F + (i % 2) * .2F, -2.2F + i * 1.3F, 1.8F, 1.4F, 1.5F, 1.5F));
        if (variant == 9) for (int i = 0; i < 5; i++) cubes.add(box("crown_" + i, HEAD, 2,
            -4.2F + i * 1.65F, -7.75F, -4.7F, 1.6F, .75F, .8F));
        var ornaments = variant >= 5 ? List.of(layer(id + "_pin", HAIR_ORNAMENT,
            cloth("pin", HEAD, 3, ROLE_HARDWARE, 3.95F, -5.7F, 2.7F, .45F, .8F, .5F))) : List.<ClothingLayer>of();
        return new HairModel(id, ALL, cubes, ornaments);
    }
    private OutfitCatalog() {}
}
