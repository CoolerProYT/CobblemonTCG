package com.coolerpromc.cobblemontcg.villager;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.ModBlocks;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.ai.village.poi.PoiType;
import net.minecraft.world.entity.npc.VillagerProfession;

public class ModVillagers {
    public static final ResourceKey<PoiType> CARD_DEALER_POI_KEY = ResourceKey.create(Registries.POINT_OF_INTEREST_TYPE, Constants.id("card_dealer"));

    public static final RegistryHandler<PoiType, PoiType> CARD_DEALER_POI = Services.REGISTRY.registerPoiType("card_dealer", ModBlocks.CARD_DEALER_TABLE, 1, 1);
    public static final RegistryHandler<VillagerProfession, VillagerProfession> CARD_DEALER = Services.REGISTRY.registerVillagerProfession("card_dealer", CARD_DEALER_POI_KEY, SoundEvents.VILLAGER_WORK_LIBRARIAN);

    public static void init(){
        Constants.LOG.info("Registering villager professions.");
    }
}
