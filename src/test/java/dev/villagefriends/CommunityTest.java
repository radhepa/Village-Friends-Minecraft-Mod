package dev.villagefriends;

import static org.junit.jupiter.api.Assertions.*;
import com.google.gson.JsonParser;
import com.mojang.serialization.JsonOps;
import java.util.*;
import net.minecraft.core.BlockPos;
import org.junit.jupiter.api.Test;

class CommunityTest {
    @Test void villageRegistryAndHometownsPersistAcrossRenamingAndMarkerRemoval() {
        var a=new VillageRecord("marker:0:64:0","Willowhaven",0,64,0,96,true,0,64,0);
        var b=new VillageRecord("marker:300:64:0","Oakbrook",300,64,0,96,false,0,0,0);
        var book=VillageBook.EMPTY.put(a).put(b);
        assertEquals(a,book.at(new BlockPos(2,65,4)));assertNull(book.at(new BlockPos(160,64,0)));
        var renamed=a.marker(new BlockPos(5,64,8),"Fernford").unmarked();book=book.put(renamed);
        assertEquals(a.id(),renamed.id());assertFalse(renamed.marked());
        assertEquals(book,VillageBook.CODEC.parse(JsonOps.INSTANCE,VillageBook.CODEC.encodeStart(JsonOps.INSTANCE,book).getOrThrow()).getOrThrow());
        var home=new ResidentHome(a.id(),"Liora Ash","minecraft:overworld");
        assertEquals(home,ResidentHome.CODEC.parse(JsonOps.INSTANCE,ResidentHome.CODEC.encodeStart(JsonOps.INSTANCE,home).getOrThrow()).getOrThrow());
        assertEquals("Liora Ash of Fernford",VillageNames.label(home.baseName(),renamed.name()));
    }
    @Test void villageNamesAreStableReadableAndSanitizeAnvilInput() {
        assertEquals(VillageNames.generate(25,128,-96),VillageNames.generate(25,128,-96));
        assertTrue(VillageNames.generate(25,128,-96).matches("[A-Za-z]+"));
        var names=new HashSet<String>();for(int x=0;x<100;x++)names.add(VillageNames.generate(25,x*500,x*23));assertTrue(names.size()>50);
        assertEquals("Willow Brook",VillageNames.clean("  Willow   Brook\n"));
        assertEquals("abcdef",VillageNames.clean("abc\u0000def"));
    }
    @Test void appearanceUsesTheNewDeterministicRecipe() {
        UUID id=UUID.fromString("9c5aeb8b-4ff4-4785-b28e-2b946cc583bf");
        String recipe=ResidentAppearance.generate(id);
        assertEquals(recipe, ResidentProfile.generate(id, "").look());
        assertEquals(recipe, ResidentProfile.generate(id, recipe).look());
        assertNotNull(dev.villagefriends.outfit.ResidentLook.parse(recipe));
        assertEquals(recipe, ResidentProfile.generate(id, "retired-wardrobe").look());
    }
}

