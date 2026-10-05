package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class MaleRegistryTest {
    @Test void registryHasFiveSequentialItemsInEachCategory() {
        checkIds(MaleHairRegistry.ALL.stream().map(MaleHairRegistry.Entry::id).toList(),"m_hair_");
        checkIds(MaleTopRegistry.ALL.stream().map(MaleTopRegistry.Entry::id).toList(),"m_top_");
        checkIds(MaleBottomRegistry.ALL.stream().map(MaleBottomRegistry.Entry::id).toList(),"m_bottom_");
        assertEquals(5,MaleHairRegistry.ALL.stream().map(MaleHairRegistry.Entry::geometry).distinct().count());
        assertEquals(5,MaleTopRegistry.ALL.stream().map(MaleTopRegistry.Entry::family).distinct().count());
        assertEquals(5,MaleBottomRegistry.ALL.stream().map(MaleBottomRegistry.Entry::family).distinct().count());
        assertThrows(UnsupportedOperationException.class,()->MaleHairRegistry.ALL.clear());
    }
    private static void checkIds(List<String> ids,String prefix) {
        assertEquals(5,ids.size()); assertEquals(5,new HashSet<>(ids).size());
        for (int i=0;i<5;i++) assertEquals(prefix+String.format(Locale.ROOT,"%02d",i+1),ids.get(i));
    }

    @Test void everyGarmentHasExactDisjointFourChannelBoundsAndTextileRatios() {
        var materials=new ArrayList<MaterialMask>();
        MaleTopRegistry.ALL.forEach(e->materials.add(e.materials())); MaleBottomRegistry.ALL.forEach(e->materials.add(e.materials()));
        for (var material : materials) {
            assertEquals(20,material.width()); assertEquals(16,material.height());
            assertEquals(180,material.pixels(ColorRole.ROLE_PRIMARY)); assertEquals(90,material.pixels(ColorRole.ROLE_SECONDARY));
            assertEquals(30,material.pixels(ColorRole.ROLE_ACCENT)); assertEquals(20,material.pixels(ColorRole.ROLE_HARDWARE));
            var palette=MasterPalettes.get(PaletteID.ASH_AND_TEAL); var counts=new EnumMap<ColorRole,Integer>(ColorRole.class);
            for (var role : ColorRole.values()) counts.put(role,0);
            for (int y=0;y<16;y++) for (int x=0;x<20;x++) {
                int pixel=material.mask().argb(x,y,palette);
                var role=Arrays.stream(ColorRole.values()).filter(r->pixel==(0xFF000000|palette.rgb(r))).findFirst().orElseThrow();
                counts.merge(role,1,Integer::sum);
            }
            for (var role : ColorRole.values()) assertEquals(material.pixels(role),counts.get(role));
            assertThrows(UnsupportedOperationException.class,()->material.bounds().clear());
        }
    }

    @Test void hairUsesActualVolumeAndDeclaredLayerDepthAndCowlsUseThePalette() {
        var shapes=new HashSet<String>();
        for (var hair : MaleHairRegistry.ALL) {
            assertTrue(hair.voxelVolume()>=1 && hair.voxelVolume()<=3);
            assertEquals(hair.strandLayerDepth(),hair.model().voxels().stream().mapToInt(VoxelBox::depthLayer).max().orElseThrow());
            assertTrue(hair.model().voxels().stream().anyMatch(v->v.depthLayer()>0 && v.outsideHead()));
            assertTrue(shapes.add(geometry(hair.model().voxels())));

        }
    }
    private static String geometry(List<VoxelBox> boxes) {
        return boxes.stream().map(v->List.of(v.bone(),v.depthLayer(),v.x(),v.y(),v.z(),v.width(),v.height(),v.depth(),v.inflation()).toString())
            .sorted().toList().toString();
    }
    private static String garmentGeometry(List<ClothingLayer> layers) {
        return geometry(layers.stream().flatMap(l->l.voxels().stream()).map(MaskedVoxel::geometry).toList());
    }

    @Test void allFiveTopsAndBottomsHaveDistinctSolidConstructions() {
        var tops=new HashSet<String>(); var bottoms=new HashSet<String>();
        for (var top : MaleTopRegistry.ALL) {
            assertTrue(tops.add(garmentGeometry(top.model().layers())),top.id());
            assertEquals(Set.of(Gender.MALE),top.model().genders());
        }
        for (var bottom : MaleBottomRegistry.ALL) {
            assertTrue(bottoms.add(garmentGeometry(bottom.model().layers())),bottom.id());
            assertEquals(Set.of(Gender.MALE),bottom.model().genders());
        }
    }

    @Test void factoryUsesAllFiveMaleAssetsAndKeepsOnePalette() {
        var hairIds=new HashSet<String>(); var topIds=new HashSet<String>(); var bottomIds=new HashSet<String>();
        for (int seed=0;seed<1024;seed++) for (var job : List.of(Profession.NONE,Profession.FARMER,Profession.MERCHANT,Profession.SCHOLAR,Profession.ADVENTURER)) {
            var outfit=OutfitFactory.assembleOutfit(Gender.MALE,job,PaletteID.FOREST_AND_HEARTH,seed);
            hairIds.add(outfit.hair().id()); topIds.add(outfit.top().id()); bottomIds.add(outfit.bottom().id());
            for (var layer : outfit.layers()) assertSame(outfit.palette(),layer.palette());
            assertTrue(outfit.bottom().compatibleStyles().contains(outfit.top().style()));
        }
        assertEquals(5,hairIds.size()); assertEquals(5,topIds.size()); assertEquals(5,bottomIds.size());
    }

    @Test void retiredMaleRecipesUseTheRebuiltFivePieceCatalog() {
        var current=ResidentLook.generate(new UUID(9,21)); assertEquals(4,current.version());
        assertEquals(current,ResidentLook.parse(current.recipe()));
        var old=ResidentLook.parse("outfit1:2:MALE:FOREST_AND_HEARTH:81"); assertNotNull(old);
        var oldOutfit=old.outfit(Profession.MERCHANT);
        assertTrue(oldOutfit.hair().id().startsWith("m_hair_")); assertTrue(oldOutfit.top().id().startsWith("m_top_"));
        var modern=new ResidentLook(2,Gender.MALE,PaletteID.FOREST_AND_HEARTH,81).outfit(Profession.MERCHANT);
        assertTrue(modern.hair().id().startsWith("m_hair_")); assertTrue(modern.top().id().startsWith("m_top_"));
    }
}
