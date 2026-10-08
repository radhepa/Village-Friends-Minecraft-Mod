package dev.villagefriends.pet;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

/** Kept on a resident: the pet they adopted (its entity UUID), what it is, its name and the game day it came home. */
public record PetLink(String pet, String species, String name, long since) {
    public static final Codec<PetLink> CODEC = RecordCodecBuilder.create(i -> i.group(
            Codec.STRING.fieldOf("pet").forGetter(PetLink::pet),
            Codec.STRING.fieldOf("species").forGetter(PetLink::species),
            Codec.STRING.fieldOf("name").forGetter(PetLink::name),
            Codec.LONG.optionalFieldOf("since", 0L).forGetter(PetLink::since)
    ).apply(i, PetLink::new));
    public String describe() { return name + " the " + species; }
}
