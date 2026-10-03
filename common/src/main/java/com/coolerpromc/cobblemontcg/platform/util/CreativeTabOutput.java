package com.coolerpromc.cobblemontcg.platform.util;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;

import java.util.Collection;

@FunctionalInterface
public interface CreativeTabOutput {
    void accept(ItemStack itemStack);

    default void accept(ItemLike itemLike){
        accept(new ItemStack(itemLike));
    }

    default void acceptAll(Collection<ItemStack> itemStacks){
        itemStacks.forEach(this::accept);
    }
}
