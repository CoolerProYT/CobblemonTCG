package com.coolerpromc.cobblemontcg.tcg.card;

import com.coolerpromc.cobblemontcg.Constants;
import com.mojang.serialization.Codec;
import net.minecraft.util.StringRepresentable;

public enum CardSupertype implements StringRepresentable {
    POKEMON("pokemon"),
    TRAINER("trainer"),
    ENERGY("energy");

    public static final Codec<CardSupertype> CODEC = StringRepresentable.fromEnum(CardSupertype::values);

    private final String name;

    CardSupertype(String name) {
        this.name = name;
    }

    public String translationKey() {
        return "supertype." + Constants.MODID + "." + name;
    }

    @Override
    public String getSerializedName() {
        return name;
    }
}
