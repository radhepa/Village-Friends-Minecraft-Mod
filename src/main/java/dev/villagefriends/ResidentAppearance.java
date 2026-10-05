package dev.villagefriends;

import dev.villagefriends.outfit.ResidentLook;
import java.util.UUID;

public final class ResidentAppearance {
    public static String generate(UUID id) { return ResidentLook.generate(id).recipe(); }
    public static int complexion(String recipe) {
        var look = ResidentLook.parse(recipe);
        return look == null ? 0 : look.complexion();
    }
    private ResidentAppearance() {}
}
