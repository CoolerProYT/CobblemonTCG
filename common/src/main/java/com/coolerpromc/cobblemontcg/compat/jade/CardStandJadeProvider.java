package com.coolerpromc.cobblemontcg.compat.jade;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.phys.Vec2;
import snownee.jade.api.BlockAccessor;
import snownee.jade.api.IBlockComponentProvider;
import snownee.jade.api.ITooltip;
import snownee.jade.api.config.IPluginConfig;
import snownee.jade.api.ui.IElementHelper;

public enum CardStandJadeProvider implements IBlockComponentProvider {
    INSTANCE;

    private static final ResourceLocation UID = Constants.id("card_display_stand");
    private static final String KEY = "jade." + Constants.MODID + ".card_display_stand.";
    private static final Vec2 ITEM_OFFSET = new Vec2(0, -2);

    @Override
    public void appendTooltip(ITooltip tooltip, BlockAccessor accessor, IPluginConfig config) {
        if (!(accessor.getBlockEntity() instanceof CardDisplayStandBlockEntity stand)) {
            return;
        }
        IElementHelper elements = IElementHelper.get();
        ItemStack card = stand.card();
        if (card.isEmpty()) {
            tooltip.add(Component.translatable(KEY + "empty").withStyle(ChatFormatting.GRAY));
        } else {
            tooltip.add(elements.smallItem(card).translate(ITEM_OFFSET));
            tooltip.append(Component.translatable(KEY + "card", card.getHoverName(), card.getCount()));
            if (stand.isForSale()) {
                ItemStack price = stand.priceItem();
                tooltip.add(Component.translatable(KEY + "price").withStyle(ChatFormatting.GRAY));
                tooltip.append(elements.smallItem(price).translate(ITEM_OFFSET));
                tooltip.append(Component.translatable(KEY + "price_amount", stand.priceAmount(), price.getHoverName()).withStyle(ChatFormatting.GOLD));
            } else {
                tooltip.add(Component.translatable(KEY + "not_for_sale").withStyle(ChatFormatting.GRAY));
            }
        }
        if (stand.hasOwner()) {
            tooltip.add(Component.translatable(KEY + "seller", stand.ownerName()).withStyle(ChatFormatting.GRAY));
        }
    }

    @Override
    public ResourceLocation getUid() {
        return UID;
    }
}
