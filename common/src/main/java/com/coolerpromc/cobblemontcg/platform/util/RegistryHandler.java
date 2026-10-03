package com.coolerpromc.cobblemontcg.platform.util;

import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponentType;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;

import java.util.function.Supplier;

public interface RegistryHandler<R, T extends R> extends Supplier<T> {
    Holder<R> holder();

    default ResourceKey<R> key(){
        return holder().unwrapKey().orElse(null);
    }

    default ResourceLocation id(){
        return key().location();
    }

    @Override
    @SuppressWarnings("unchecked")
    default T get(){
        return (T) holder().value();
    }

    interface Items<I extends Item> extends RegistryHandler<Item, I>, ItemLike {
        @Override
        default Item asItem(){
            return get();
        }

        default ItemStack toStack(){
            return new ItemStack(asItem());
        }
    }

    interface Components<T> extends RegistryHandler<DataComponentType<?>, DataComponentType<T>>{
    }
}
