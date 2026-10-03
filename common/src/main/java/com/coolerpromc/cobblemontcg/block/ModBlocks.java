package com.coolerpromc.cobblemontcg.block;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.custom.CardDealerTableBlock;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.platform.Services;
import com.coolerpromc.cobblemontcg.platform.util.RegistryHandler;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.block.state.properties.NoteBlockInstrument;
import net.minecraft.world.level.material.MapColor;

import java.util.function.Function;

public class ModBlocks {
    public static final RegistryHandler.Blocks<CardDealerTableBlock> CARD_DEALER_TABLE = registerBlock("card_dealer_table", CardDealerTableBlock::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.WOOD).instrument(NoteBlockInstrument.BASS).strength(2.5F).sound(SoundType.WOOD).ignitedByLava());
    public static final RegistryHandler.Items<BlockItem> CARD_DEALER_TABLE_ITEM = ModItems.registerItem("card_dealer_table", p -> new BlockItem(CARD_DEALER_TABLE.get(), p));

    public static <T extends Block> RegistryHandler.Blocks<T> registerBlock(String name, Function<BlockBehaviour.Properties, T> func, BlockBehaviour.Properties p){
        return Services.REGISTRY.registerBlock(name, func, p);
    }

    public static void init(){
        Constants.LOG.info("Registering blocks.");
    }
}
