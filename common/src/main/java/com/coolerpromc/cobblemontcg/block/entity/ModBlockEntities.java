package com.coolerpromc.cobblemontcg.block.entity;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.ModBlocks;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.world.level.block.entity.BlockEntityType;

public class ModBlockEntities {
    public static final RegistryHandler<BlockEntityType<?>, BlockEntityType<CardDisplayStandBlockEntity>> CARD_DISPLAY_STAND =
            Services.REGISTRY.registerBlockEntityType("card_display_stand", CardDisplayStandBlockEntity::new, ModBlocks.CARD_DISPLAY_STAND);

    public static void init(){
        Constants.LOG.info("Registering block entities.");
    }
}
