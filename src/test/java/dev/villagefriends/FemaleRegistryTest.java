package dev.villagefriends;

import dev.villagefriends.outfit.*;
import java.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class FemaleRegistryTest {
    @Test void registryContainsExactlyFiftySequentialItemsPerCategory() {
        checkIds(FemaleHairRegistry.ALL.stream().map(FemaleHairRegistry.Entry::id).toList(),"f_hair_");
        checkIds(FemaleTopRegistry.ALL.stream().map(FemaleTopRegistry.Entry::id).toList(),"f_top_");
        checkIds(FemaleBottomRegistry.ALL.stream().map(FemaleBottomRegistry.Entry::id).toList(),"f_bottom_");
        assertEquals(10,FemaleHairRegistry.ALL.stream().map(FemaleHairRegistry.Entry::geometry).distinct().count());
        assertEquals(6,FemaleTopRegistry.ALL.stream().map(FemaleTopRegistry.Entry::family).distinct().count());
        assertEquals(5,FemaleBottomRegistry.ALL.stream().map(FemaleBottomRegistry.Entry::family).distinct().count());
        assertThrows(UnsupportedOperationException.class,()->FemaleHairRegistry.ALL.clear());
        assertThrows(UnsupportedOperationException.class,()->FemaleBottomRegistry.ALL.getFirst().styles().clear());
    }
    private static void checkIds(List<String> ids,String prefix) {
        assertEquals(50,ids.size()); assertEquals(50,new HashSet<>(ids).size());
        for (int i=0;i<50;i++) assertEquals(prefix+String.format(Locale.ROOT,"%02d",i+1),ids.get(i));
    }
    private static String geometry(List<VoxelBox> boxes) {
        return boxes.stream().map(v->List.of(v.bone(),v.depthLayer(),v.x(),v.y(),v.z(),v.width(),v.height(),v.depth(),v.inflation()).toString())
            .sorted().toList().toString();
    }
    private static String garmentGeometry(List<ClothingLayer> layers) {
        return geometry(layers.stream().flatMap(l->l.voxels().stream()).map(MaskedVoxel::geometry).toList());
    }
    @Test void everyHairHasDistinctSolidLayersAndItsDeclaredBackLength() {
        var shapes=new HashSet<String>();
        for (var hair:FemaleHairRegistry.ALL) {
            assertEquals(Set.of(Gender.FEMALE),hair.model().genders());
            assertTrue(hair.voxelVolume()>=1 && hair.voxelVolume()<=3);
            assertEquals(hair.strandLayerDepth(),hair.model().voxels().stream().mapToInt(VoxelBox::depthLayer).max().orElseThrow());
            assertEquals(hair.backLength(),hair.model().voxels().stream().mapToDouble(v->v.y()+v.height()).max().orElseThrow(),.00001,hair.id());
            assertTrue(hair.model().voxels().stream().anyMatch(v->v.depthLayer()>0 && v.outsideHead()));
            assertTrue(shapes.add(geometry(hair.model().voxels())),hair.id());
            for (var v:hair.model().voxels()) {
                assertEquals(BodyPart.HEAD,v.bone()); assertTrue(v.width()>0 && v.height()>0 && v.depth()>0);
            }
            for (var ornament:hair.model().ornaments()) for (var voxel:ornament.voxels())
                assertTrue(voxel.mask().weights()[0]==0x0000FF00 || voxel.mask().weights()[0]==0x000000FF);
        }
    }
    @Test void allGarmentsHaveExactRoleBoundsAndCorrespondingPaletteComponents() {
        for (var top:FemaleTopRegistry.ALL) checkMaterial(top.materials(),top.model().layers());
        for (var bottom:FemaleBottomRegistry.ALL) checkMaterial(bottom.materials(),bottom.model().layers());
    }
    private static void checkMaterial(MaterialMask mask,List<ClothingLayer> layers) {
        assertEquals(20,mask.width()); assertEquals(16,mask.height());
        var palette=MasterPalettes.get(PaletteID.ROYAL_VELVET); var counts=new EnumMap<ColorRole,Integer>(ColorRole.class);
        for (var role:ColorRole.values()) counts.put(role,0);
        var coverage=new HashSet<String>();
        for (var role:ColorRole.values()) for (var b:mask.bounds().get(role)) {
            for (int y=b.y0();y<b.y1();y++) for (int x=b.x0();x<b.x1();x++) {
                assertTrue(coverage.add(x+":"+y)); assertEquals(0xFF000000|palette.rgb(role),mask.mask().argb(x,y,palette));
                counts.merge(role,1,Integer::sum);
            }
        }
        assertEquals(320,coverage.size());
        assertEquals(Map.of(ColorRole.ROLE_PRIMARY,180,ColorRole.ROLE_SECONDARY,90,ColorRole.ROLE_ACCENT,30,ColorRole.ROLE_HARDWARE,20),counts);
        var components=new HashSet<Integer>(); layers.forEach(l->l.voxels().forEach(v->components.add(v.mask().weights()[0])));
        assertEquals(Set.of(0xFF000000,0x00FF0000,0x0000FF00,0x000000FF),components);
        assertThrows(UnsupportedOperationException.class,()->mask.bounds().clear());
    }
    @Test void everyTopAndBottomHasDistinctConstructionAndFemaleEligibility() {
        var tops=new HashSet<String>(); var bottoms=new HashSet<String>();
        for (var top:FemaleTopRegistry.ALL) {
            assertTrue(tops.add(garmentGeometry(top.model().layers())),top.id()); assertEquals(Set.of(Gender.FEMALE),top.model().genders());
        }
        for (var bottom:FemaleBottomRegistry.ALL) {
            assertTrue(bottoms.add(garmentGeometry(bottom.model().layers())),bottom.id()); assertEquals(Set.of(Gender.FEMALE),bottom.model().genders());
        }
        assertEquals(15,OutfitCatalog.ALL_HAIR.size()); assertEquals(15,OutfitCatalog.ALL_TOPS.size()); assertEquals(11,OutfitCatalog.ALL_BOTTOMS.size());
    }
}
