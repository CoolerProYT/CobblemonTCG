package com.coolerpromc.cobblemontcg.tcg.card;

import com.coolerpromc.cobblemontcg.Constants;
import com.mojang.serialization.Codec;
import net.minecraft.ChatFormatting;
import net.minecraft.util.StringRepresentable;

public enum CardRarity implements StringRepresentable {
    COMMON("common", ChatFormatting.WHITE),
    UNCOMMON("uncommon", ChatFormatting.GREEN),
    RARE("rare", ChatFormatting.AQUA),
    RARE_HOLO("rare_holo", ChatFormatting.LIGHT_PURPLE);

    public static final Codec<CardRarity> CODEC = StringRepresentable.fromEnum(CardRarity::values);

    private final String name;
    private final ChatFormatting color;

    CardRarity(String name, ChatFormatting color) {
        this.name = name;
        this.color = color;
    }

    public ChatFormatting color() {
        return color;
    }

    public boolean isHolo() {
        return this == RARE_HOLO;
    }

    public String translationKey() {
        return "rarity." + Constants.MODID + "." + name;
    }

    @Override
    public String getSerializedName() {
        return name;
    }
}
