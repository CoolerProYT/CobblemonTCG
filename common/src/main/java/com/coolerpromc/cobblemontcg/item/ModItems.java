package com.coolerpromc.cobblemontcg.item;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.item.custom.BoosterPackItem;
import com.coolerpromc.cobblemontcg.item.custom.TcgCardItem;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.world.item.Item;

import java.util.function.Function;

public class ModItems {
    public static final RegistryHandler.Items<BoosterPackItem> BOOSTER_PACK = registerItem("booster_pack", p -> new BoosterPackItem(p.stacksTo(16)));
    public static final RegistryHandler.Items<TcgCardItem> TCG_CARD = registerItem("tcg_card", p -> new TcgCardItem(p.stacksTo(64)));

    public static <T extends Item> RegistryHandler.Items<T> registerItem(String name, Function<Item.Properties, T> func){
        return Services.REGISTRY.registerItem(name, func);
    }

    public static void init(){
        Constants.LOG.info("Registering items.");
    }
}
