package com.coolerpromc.cobblemontcg.item.custom;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.TcgCardData;
import com.coolerpromc.cobblemontcg.tcg.card.CardDefinition;
import com.coolerpromc.cobblemontcg.tcg.card.CardSupertype;
import com.coolerpromc.cobblemontcg.tcg.data.TcgDataManager;
import com.coolerpromc.cobblemontcg.tcg.set.TcgSet;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

import java.util.List;
import java.util.Locale;
import java.util.Optional;

public class TcgCardItem extends Item {
    private static final String TOOLTIP = "tooltip." + Constants.MODID + ".card.";

    public TcgCardItem(Properties properties) {
        super(properties);
    }

    @Override
    public Component getName(ItemStack stack) {
        return lookup(stack)
                .<Component>map(card -> Component.literal(card.name()).withStyle(card.rarity().color()))
                .orElseGet(() -> super.getName(stack));
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        TcgCardData data = stack.get(ModDataComponents.TCG_CARD.get());
        if (data == null) {
            return;
        }
        Optional<TcgSet> set = TcgDataManager.forDisplay().set(data.setId());
        Optional<CardDefinition> card = set.flatMap(s -> s.card(data.cardNumber()));
        if (set.isEmpty() || card.isEmpty()) {
            tooltip.add(Component.translatable(TOOLTIP + "unknown").withStyle(ChatFormatting.RED));
            return;
        }
        CardDefinition definition = card.get();

        tooltip.add(Component.translatable(TOOLTIP + "number", definition.number(), set.get().definition().total(), set.get().definition().name()).withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable(TOOLTIP + "rarity", Component.translatable(definition.rarity().translationKey()).withStyle(definition.rarity().color())).withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable(TOOLTIP + "supertype", Component.translatable(definition.supertype().translationKey())).withStyle(ChatFormatting.GRAY));
        definition.hp().ifPresent(hp -> tooltip.add(Component.translatable(TOOLTIP + "hp", hp).withStyle(ChatFormatting.GRAY)));
        if (definition.supertype() != CardSupertype.TRAINER) {
            definition.type().ifPresent(type -> tooltip.add(Component.translatable(TOOLTIP + "type", typeName(type)).withStyle(ChatFormatting.GRAY)));
        }
        if (data.holo()) {
            tooltip.add(Component.translatable(TOOLTIP + "holo").withStyle(ChatFormatting.GOLD));
        }
    }

    private static Optional<CardDefinition> lookup(ItemStack stack) {
        TcgCardData data = stack.get(ModDataComponents.TCG_CARD.get());
        return data == null ? Optional.empty() : TcgDataManager.forDisplay().card(data.setId(), data.cardNumber());
    }

    private static MutableComponent typeName(String type) {
        String fallback = type.isEmpty() ? type : type.substring(0, 1).toUpperCase(Locale.ROOT) + type.substring(1);
        return Component.translatableWithFallback("type." + Constants.MODID + "." + type, fallback);
    }
}
