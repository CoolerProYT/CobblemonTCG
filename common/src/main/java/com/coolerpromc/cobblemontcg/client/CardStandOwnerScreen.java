package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import com.coolerpromc.cobblemontcg.menu.CardStandOwnerMenu;
import com.coolerpromc.cobblemontcg.network.ServerboundSetStandPricePacket;
import com.coolerpromc.cobblemontcg.platform.Services;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.components.Tooltip;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.Rect2i;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;

import java.util.ArrayList;
import java.util.List;

public class CardStandOwnerScreen extends CardStandScreen<CardStandOwnerMenu> {
    private static final int RIGHT_X = 60;
    private static final int RIGHT_WIDTH = 108;
    private static final int AMOUNT_Y = CardStandOwnerMenu.PRICE_Y;

    public static boolean jeiPresent = false;

    private EditBox amountBox;
    private Button collectButton;
    private int shownAmount = -1;

    public CardStandOwnerScreen(CardStandOwnerMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title, Constants.id("textures/gui/card_display_stand_owner.png"));
    }

    @Override
    protected int cardSlot() {
        return CardStandOwnerMenu.CARD_SLOT;
    }

    @Override
    protected void init() {
        super.init();
        int x = leftPos;
        int y = topPos;
        addRenderableWidget(Button.builder(Component.literal("-"), b -> nudge(-1))
                .bounds(x + 80, y + AMOUNT_Y - 1, 14, 18).tooltip(Tooltip.create(Component.translatable(KEY + "nudge"))).build());
        amountBox = new EditBox(font, x + 97, y + AMOUNT_Y + 4, 34, 12, Component.translatable(KEY + "amount"));
        amountBox.setBordered(false);
        amountBox.setTextColor(0xFFFFFF);
        amountBox.setMaxLength(String.valueOf(CardDisplayStandBlockEntity.MAX_PRICE).length());
        amountBox.setFilter(text -> text.chars().allMatch(Character::isDigit));
        amountBox.setValue(String.valueOf(menu.priceAmount()));
        amountBox.setResponder(this::typed);
        addRenderableWidget(amountBox);
        addRenderableWidget(Button.builder(Component.literal("+"), b -> nudge(1))
                .bounds(x + 134, y + AMOUNT_Y - 1, 14, 18).tooltip(Tooltip.create(Component.translatable(KEY + "nudge"))).build());
        collectButton = addRenderableWidget(Button.builder(Component.translatable(KEY + "collect"), b -> pressButton(CardStandOwnerMenu.BUTTON_COLLECT))
                .bounds(x + 116, y + CardStandOwnerMenu.TILL_Y - 1, 52, 18).build());
        shownAmount = menu.priceAmount();
    }

    public Rect2i priceArea() {
        return new Rect2i(leftPos + CardStandOwnerMenu.PRICE_X - 1, topPos + CardStandOwnerMenu.PRICE_Y - 1, 18, 18);
    }

    public void setPriceItem(ItemStack item) {
        Services.NETWORK.sendToServer(new ServerboundSetStandPricePacket(menu.containerId, item.copyWithCount(1)));
    }

    private void nudge(int direction) {
        int step = Screen.hasShiftDown() ? 10 : 1;
        setAmount(menu.priceAmount() + direction * step);
        amountBox.setValue(String.valueOf(shownAmount));
    }

    private void typed(String text) {
        if (text.isEmpty()) {
            return;
        }
        try {
            setAmount(Integer.parseInt(text));
        } catch (NumberFormatException ignored) {
        }
    }

    private void setAmount(int amount) {
        int clamped = Math.clamp(amount, 1, CardDisplayStandBlockEntity.MAX_PRICE);
        if (clamped != shownAmount) {
            shownAmount = clamped;
            pressButton(CardStandOwnerMenu.BUTTON_AMOUNT + clamped);
        }
    }

    @Override
    protected void containerTick() {
        super.containerTick();
        int amount = menu.priceAmount();
        if (!amountBox.isFocused() && (amount != shownAmount || amountBox.getValue().isEmpty())) {
            shownAmount = amount;
            amountBox.setValue(String.valueOf(amount));
        }
        collectButton.active = menu.tillKinds() > 0;
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderLabels(graphics, mouseX, mouseY);
        graphics.drawString(font, Component.translatable(KEY + "price_label"), RIGHT_X, CardStandOwnerMenu.PRICE_Y - 12, TEXT, false);

        ItemStack price = menu.getSlot(CardStandOwnerMenu.PRICE_SLOT).getItem();
        ItemStack card = menu.getSlot(CardStandOwnerMenu.CARD_SLOT).getItem();
        Component status;
        int color;
        if (price.isEmpty()) {
            status = Component.translatable(KEY + "status.no_price");
            color = TEXT_BAD;
        } else if (card.isEmpty()) {
            status = Component.translatable(KEY + "status.no_card");
            color = TEXT_MUTED;
        } else {
            status = Component.translatable(KEY + "status.selling", menu.priceAmount(), price.getHoverName());
            color = TEXT_GOOD;
        }
        graphics.drawString(font, trimmed(status, RIGHT_WIDTH), RIGHT_X, CardStandOwnerMenu.PRICE_Y + 21, color, false);

        graphics.drawString(font, Component.translatable(KEY + "till_label"), RIGHT_X, CardStandOwnerMenu.TILL_Y - 12, TEXT, false);
        if (menu.tillKinds() > 0) {
            graphics.drawString(font, Component.translatable(KEY + "count", menu.tillTotal()), RIGHT_X + 20, CardStandOwnerMenu.TILL_Y + 4, TEXT, false);
        } else {
            graphics.drawString(font, Component.translatable(KEY + "till_empty"), RIGHT_X + 20, CardStandOwnerMenu.TILL_Y + 4, TEXT_MUTED, false);
        }
    }

    @Override
    protected void renderTooltip(GuiGraphics graphics, int x, int y) {
        if (menu.getCarried().isEmpty() && hoveredSlot != null) {
            if (hoveredSlot.index == CardStandOwnerMenu.PRICE_SLOT) {
                List<Component> lines = new ArrayList<>();
                if (hoveredSlot.hasItem()) {
                    lines.addAll(getTooltipFromContainerItem(hoveredSlot.getItem()));
                    lines.add(Component.translatable(KEY + "price_hint.clear").withStyle(s -> s.withColor(0xA0A0A0)));
                } else {
                    lines.add(Component.translatable(KEY + "price_hint.set"));
                    if (jeiPresent) {
                        lines.add(Component.translatable(KEY + "price_hint.jei").withStyle(s -> s.withColor(0xA0A0A0)));
                    }
                }
                graphics.renderComponentTooltip(font, lines, x, y);
                return;
            }
            if (hoveredSlot.index == CardStandOwnerMenu.TILL_SLOT && hoveredSlot.hasItem()) {
                List<Component> lines = new ArrayList<>(getTooltipFromContainerItem(hoveredSlot.getItem()));
                if (menu.tillKinds() > 1) {
                    lines.add(Component.translatable(KEY + "till_kinds", menu.tillKinds()).withStyle(s -> s.withColor(0xA0A0A0)));
                }
                graphics.renderComponentTooltip(font, lines, x, y);
                return;
            }
            if (hoveredSlot.index == CardStandOwnerMenu.CARD_SLOT && !hoveredSlot.hasItem()) {
                graphics.renderTooltip(font, Component.translatable(KEY + "card_hint"), x, y);
                return;
            }
        }
        super.renderTooltip(graphics, x, y);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (amountBox.isFocused() && keyCode != GLFW.GLFW_KEY_ESCAPE) {
            if (keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER) {
                amountBox.setFocused(false);
                setFocused(null);
                return true;
            }
            return amountBox.keyPressed(keyCode, scanCode, modifiers) || amountBox.canConsumeInput();
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }
}
