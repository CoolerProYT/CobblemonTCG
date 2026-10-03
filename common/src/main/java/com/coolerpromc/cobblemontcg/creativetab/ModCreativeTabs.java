package com.coolerpromc.cobblemontcg.creativetab;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.SetDefinition;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import com.coolerpromc.cobblemontcg.util.TcgStacks;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;

public class ModCreativeTabs {
    public static final RegistryHandler<CreativeModeTab, CreativeModeTab> TAB = Services.REGISTRY.registerCreativeTab(Constants.MODID, ModItems.BOOSTER_PACK::toStack, Component.translatable("itemGroup." + Constants.MODID), (output, parameters) -> {
        for (TcgSet set : TcgDataManager.forDisplay().sets()) {
            for (String wrapper : set.definition().wrappers().isEmpty() ? java.util.List.of(SetDefinition.DEFAULT_WRAPPER) : set.definition().wrappers()) {
                output.accept(TcgStacks.pack(set.id(), wrapper, 1));
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
