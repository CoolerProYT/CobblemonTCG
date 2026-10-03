package com.coolerpromc.cobblemontcg.creativetab;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.ModBlocks;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;

public class ModCreativeTabs {
    public static final RegistryHandler<CreativeModeTab, CreativeModeTab> TAB = Services.REGISTRY.registerCreativeTab(Constants.MODID, ModItems.BOOSTER_PACK::toStack, Component.translatable("itemGroup." + Constants.MODID), (output, parameters) -> {
        output.accept(ModItems.CARD_BINDER.toStack());
        output.accept(ModBlocks.CARD_DEALER_TABLE_ITEM.toStack());
        for (TcgSet set : TcgDataManager.forDisplay().sets()) {
            for (String wrapper : set.wrappers()) {
                output.accept(TcgStacks.pack(set, wrapper, 1));
            }
            for (CardDefinition card : set.cards()) {
                output.accept(TcgStacks.card(set, card.number(), card.rarity().isHolo()));
            }
        }
    });

    public static void init(){
        Constants.LOG.info("Registering creative tabs.");
    }
}
