package com.coolerpromc.cobblemontcg.util;

import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.BoosterPackData;
import com.coolerpromc.cobblemontcg.component.custom.TcgCardData;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomModelData;

/**
 * The only place booster pack and card stacks are created, so the components always match.
 */
public final class TcgStacks {
    private TcgStacks() {
    }

    public static ItemStack pack(TcgSet set, String variant, int count) {
        ItemStack stack = new ItemStack(ModItems.BOOSTER_PACK, count);
        stack.set(ModDataComponents.BOOSTER_PACK.get(), new BoosterPackData(set.id(), variant));
        stack.set(DataComponents.CUSTOM_MODEL_DATA, new CustomModelData(set.packModelData(variant)));
        return stack;
    }

    public static ItemStack card(TcgSet set, int number, boolean holo) {
        ItemStack stack = new ItemStack(ModItems.TCG_CARD);
        stack.set(ModDataComponents.TCG_CARD.get(), new TcgCardData(set.id(), number, holo));
        stack.set(DataComponents.CUSTOM_MODEL_DATA, new CustomModelData(set.modelData(number, holo)));
        return stack;
    }
}
