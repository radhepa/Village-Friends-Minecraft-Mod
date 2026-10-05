package dev.villagefriends.client;

import dev.villagefriends.outfit.*;
import java.util.*;

/** Pixel-density face UVs: each cuboid owns an unfolded texture island with padding. */
final class OutfitAtlas {
    static final int WIDTH=512,HEIGHT=512;
    record Entry(String modelId,String kind,VoxelBox box,RoleMask mask,int index,int u,int v,int tw,int th,int td) {
        String partName() { return "outfit_"+index; }
        boolean selected(Outfit outfit) {
            return modelId.equals(switch(kind) {
                case "top" -> outfit.top().id(); case "bottom" -> outfit.bottom().id(); case "hair" -> outfit.hair().id();
                default -> throw new IllegalStateException("Invalid atlas kind");
            });
        }
    }
    private static final class Packer {
        int x,y=64,rowHeight;
        Entry add(List<Entry> entries,String id,String kind,VoxelBox box,RoleMask mask) {
            int w=Math.max(1,(int)Math.ceil(box.width())),h=Math.max(1,(int)Math.ceil(box.height())),d=Math.max(1,(int)Math.ceil(box.depth()));
            int tileW=2*(w+d)+2,tileH=h+d+2;
            if (tileW>WIDTH) throw new IllegalStateException("Oversized texture island");
            if (x+tileW>WIDTH) { x=0;y+=rowHeight;rowHeight=0; }
            if (y+tileH>HEIGHT) throw new IllegalStateException("Textured outfit atlas overflow");
            var entry=new Entry(id,kind,box,mask,entries.size(),x+1,y+1,w,h,d);
            entries.add(entry);x+=tileW;rowHeight=Math.max(rowHeight,tileH);return entry;
        }
    }
    static final List<Entry> ENTRIES;
    static {
        var entries=new ArrayList<Entry>();var pack=new Packer();
        for (var top:OutfitCatalog.ALL_TOPS) add(entries,pack,top.id(),"top",top.layers());
        for (var bottom:OutfitCatalog.ALL_BOTTOMS) add(entries,pack,bottom.id(),"bottom",bottom.layers());
        for (var hair:OutfitCatalog.ALL_HAIR) {
            for (var box:hair.voxels()) pack.add(entries,hair.id(),"hair",box,null);
            add(entries,pack,hair.id(),"hair",hair.ornaments());
        }
        ENTRIES=List.copyOf(entries);
    }
    private static void add(List<Entry> out,Packer pack,String id,String kind,List<ClothingLayer> layers) {
        for (var layer:layers) for (var voxel:layer.voxels()) pack.add(out,id,kind,voxel.geometry(),voxel.mask());
    }
    private OutfitAtlas() {}
}
