package com.coolerpromc.cobblemontcg.item.custom;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.BoosterPackData;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.pack.PackOpener;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import java.util.List;
import java.util.Optional;

public class BoosterPackItem extends Item {
    private static final int OPEN_COOLDOWN_TICKS = 10;

    public BoosterPackItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        BoosterPackData data = stack.get(ModDataComponents.BOOSTER_PACK.get());
        if (data == null) {
            return InteractionResultHolder.fail(stack);
        }
        if (level.isClientSide()) {
            return InteractionResultHolder.success(stack);
        }

        Optional<TcgSet> set = TcgDataManager.SERVER.set(data.setId());
        if (set.isEmpty()) {
            player.displayClientMessage(Component.translatable("message." + Constants.MODID + ".unknown_set", data.setId().toString()).withStyle(ChatFormatting.RED), true);
            return InteractionResultHolder.fail(stack);
        }

        PackOpener.open((ServerPlayer) player, set.get());
        player.getCooldowns().addCooldown(this, OPEN_COOLDOWN_TICKS);
        stack.consume(1, player);
        return InteractionResultHolder.success(stack);
    }

    @Override
    public Component getName(ItemStack stack) {
        BoosterPackData data = stack.get(ModDataComponents.BOOSTER_PACK.get());
        if (data != null) {
            Optional<TcgSet> set = TcgDataManager.forDisplay().set(data.setId());
            if (set.isPresent()) {
                return Component.translatable(getDescriptionId() + ".named", set.get().definition().name());
            }
        }
        return super.getName(stack);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        BoosterPackData data = stack.get(ModDataComponents.BOOSTER_PACK.get());
        if (data == null || TcgDataManager.forDisplay().set(data.setId()).isEmpty()) {
            tooltip.add(Component.translatable("tooltip." + Constants.MODID + ".unknown_set").withStyle(ChatFormatting.RED));
            return;
        }
        tooltip.add(Component.translatable("tooltip." + Constants.MODID + ".booster_pack.open").withStyle(ChatFormatting.GRAY));
        if (flag.isAdvanced()) {
            tooltip.add(Component.literal(data.setId() + " / " + data.variant()).withStyle(ChatFormatting.DARK_GRAY));
        }
    }
}
