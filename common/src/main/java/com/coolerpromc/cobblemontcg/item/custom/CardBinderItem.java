package com.coolerpromc.cobblemontcg.item.custom;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardBinderMenu;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.SimpleMenuProvider;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.ItemUtils;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.ItemContainerContents;
import net.minecraft.world.level.Level;

import java.util.List;

public class CardBinderItem extends Item {
    private static final String TOOLTIP = "tooltip." + Constants.MODID + ".card_binder.";
    private static final int OFFHAND_SLOT = Inventory.SLOT_OFFHAND;

    public CardBinderItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide()) {
            int slot = hand == InteractionHand.OFF_HAND ? OFFHAND_SLOT : player.getInventory().selected;
            player.openMenu(new SimpleMenuProvider((id, inventory, p) -> new CardBinderMenu(id, inventory, slot, stack), stack.getHoverName()));
            level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1.0F, 1.0F);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        ItemContainerContents contents = stack.getOrDefault(DataComponents.CONTAINER, ItemContainerContents.EMPTY);
        int cards = 0;
        int pockets = 0;
        for (ItemStack card : contents.nonEmptyItems()) {
            cards += card.getCount();
            pockets++;
        }
        tooltip.add(Component.translatable(TOOLTIP + "cards", cards, pockets, CardBinderMenu.CAPACITY).withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable(TOOLTIP + "open").withStyle(ChatFormatting.DARK_GRAY));
    }

    @Override
    public void onDestroyed(ItemEntity itemEntity) {
        ItemContainerContents contents = itemEntity.getItem().set(DataComponents.CONTAINER, ItemContainerContents.EMPTY);
        if (contents != null) {
            ItemUtils.onContainerDestroyed(itemEntity, contents.nonEmptyItemsCopy());
        }
    }

}
