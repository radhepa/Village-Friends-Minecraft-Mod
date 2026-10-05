package dev.villagefriends;
public final class VillageNames {
    private static final String[] FIRST = {"Willow","Oak","Amber","Clover","Silver","Moss","Maple","Hazel","Briar","Sun","Cedar","Fern","Pine","Hearth","Birch","Rose","Alder","Copper","Meadow","Honey","River","Wren","Ash","Juniper"};
    private static final String[] LAST = {"brook","haven","ridge","ford","vale","field","wick","grove","mead","hollow","bridge","crest","bend","bury","fall","well","wood","reach","hill","mere"};
    public static String generate(long seed,int x,int z) {
        long mixed=seed ^ ((long)x*341873128712L) ^ ((long)z*132897987541L);
        mixed=(mixed^(mixed>>>30))*0xbf58476d1ce4e5b9L; mixed=(mixed^(mixed>>>27))*0x94d049bb133111ebL; mixed^=mixed>>>31;
        return FIRST[Math.floorMod((int)mixed,FIRST.length)]+LAST[Math.floorMod((int)(mixed>>>32),LAST.length)];
    }
    public static String clean(String name) { return name.replaceAll("[\\p{Cntrl}§]", "").strip().replaceAll("\\s+"," "); }
    public static String label(String base, String village) { return base+" of "+village; }
    private VillageNames() {}
}
