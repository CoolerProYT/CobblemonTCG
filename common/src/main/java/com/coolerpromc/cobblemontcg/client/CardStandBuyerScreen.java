package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardStandBuyerMenu;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

public class CardStandBuyerScreen extends CardStandScreen<CardStandBuyerMenu> {
    private static final int RIGHT_X = 60;
    private static final int RIGHT_WIDTH = 108;

    private Button buyButton;

    public CardStandBuyerScreen(CardStandBuyerMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title, Constants.id("textures/gui/card_display_stand_buyer.png"));
    }

    @Override
    protected int cardSlot() {
        return CardStandBuyerMenu.CARD_SLOT;
    }

    @Override
    protected void init() {
        super.init();
        buyButton = addRenderableWidget(Button.builder(Component.translatable(KEY + "buy"), b -> pressButton(CardStandBuyerMenu.BUTTON_BUY))
                .bounds(leftPos + 116, topPos + CardStandBuyerMenu.PRICE_Y - 2, 52, 20).build());
        updateButton();
    }

    @Override
    protected void containerTick() {
        super.containerTick();
        updateButton();
    }

    private void updateButton() {
        buyButton.active = !menu.card().isEmpty() && !menu.priceItem().isEmpty() && menu.payment() >= menu.priceAmount();
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderLabels(graphics, mouseX, mouseY);
        ItemStack card = menu.card();
        ItemStack price = menu.priceItem();
        if (card.isEmpty()) {
            graphics.drawString(font, Component.translatable(KEY + "sold_out"), RIGHT_X, 20, TEXT_BAD, false);
        } else {
            graphics.drawString(font, trimmed(card.getHoverName(), RIGHT_WIDTH), RIGHT_X, 20, TEXT, false);
            graphics.drawString(font, Component.translatable(KEY + "in_stock", card.getCount()), RIGHT_X, 31, TEXT_MUTED, false);
        }

        graphics.drawString(font, Component.translatable(KEY + "price_label"), RIGHT_X, CardStandBuyerMenu.PRICE_Y - 12, TEXT, false);
        if (price.isEmpty()) {
            graphics.drawString(font, Component.translatable(KEY + "not_for_sale"), RIGHT_X + 20, CardStandBuyerMenu.PRICE_Y + 4, TEXT_MUTED, false);
            return;
        }
        graphics.drawString(font, Component.translatable(KEY + "count", menu.priceAmount()), RIGHT_X + 20, CardStandBuyerMenu.PRICE_Y + 4, TEXT, false);
        int have = menu.payment();
        int need = menu.priceAmount();
        Component status = have >= need
                ? Component.translatable(KEY + "have", have, price.getHoverName())
                : Component.translatable(KEY + "need", need - have, price.getHoverName());
        graphics.drawString(font, trimmed(status, RIGHT_WIDTH), RIGHT_X, CardStandBuyerMenu.PRICE_Y + 23, have >= need ? TEXT_GOOD : TEXT_BAD, false);
    }
}
