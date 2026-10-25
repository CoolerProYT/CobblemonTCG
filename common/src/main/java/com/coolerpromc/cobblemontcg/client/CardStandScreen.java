package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardStandMenu;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;

public abstract class CardStandScreen<M extends CardStandMenu> extends AbstractContainerScreen<M> {
    protected static final String KEY = "screen." + Constants.MODID + ".card_display_stand.";
    protected static final int TEXT = 0x404040;
    protected static final int TEXT_MUTED = 0x707070;
    protected static final int TEXT_GOOD = 0x2E7D32;
    protected static final int TEXT_BAD = 0xB02020;
    private static final float CARD_SCALE = 2.7F;

    private final ResourceLocation texture;

    protected CardStandScreen(M menu, Inventory inventory, Component title, ResourceLocation texture) {
        super(menu, inventory, title);
        this.texture = texture;
        this.imageWidth = 176;
        this.imageHeight = 202;
        this.inventoryLabelX = CardStandMenu.INVENTORY_X;
        this.inventoryLabelY = CardStandMenu.INVENTORY_Y - 11;
    }

    protected abstract int cardSlot();

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        renderTooltip(graphics, mouseX, mouseY);
    }

    @Override
    protected void renderBg(GuiGraphics graphics, float partialTick, int mouseX, int mouseY) {
        graphics.blit(texture, leftPos, topPos, 0, 0, imageWidth, imageHeight);
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        super.renderLabels(graphics, mouseX, mouseY);
        if (hoveredSlot != null && hoveredSlot.index == cardSlot()) {
            graphics.fill(RenderType.guiOverlay(), CardStandMenu.POCKET_X + 1, CardStandMenu.POCKET_Y + 1,
                    CardStandMenu.POCKET_X + CardStandMenu.POCKET_WIDTH - 1, CardStandMenu.POCKET_Y + CardStandMenu.POCKET_HEIGHT - 1, 0x50FFFFFF);
        }
    }

    @Override
    protected void renderSlot(GuiGraphics graphics, Slot slot) {
        if (slot.index != cardSlot()) {
            super.renderSlot(graphics, slot);
            return;
        }
        ItemStack stack = slot.getItem();
        if (stack.isEmpty()) {
            return;
        }
        graphics.pose().pushPose();
        graphics.pose().translate(slot.x + 8.0F, slot.y + 8.0F, 0.0F);
        graphics.pose().scale(CARD_SCALE, CARD_SCALE, 1.0F);
        graphics.pose().translate(-8.0F, -8.0F, 0.0F);
        graphics.renderItem(stack, 0, 0);
        graphics.pose().popPose();
        graphics.pose().pushPose();
        graphics.pose().translate(0.0F, 0.0F, 100.0F);
        graphics.renderItemDecorations(font, stack, CardStandMenu.POCKET_X + CardStandMenu.POCKET_WIDTH - 17, CardStandMenu.POCKET_Y + CardStandMenu.POCKET_HEIGHT - 17);
        graphics.pose().popPose();
    }

    @Override
    protected boolean isHovering(int x, int y, int width, int height, double mouseX, double mouseY) {
        if (x == CardStandMenu.CARD_X && y == CardStandMenu.CARD_Y && width == 16 && height == 16) {
            return super.isHovering(CardStandMenu.POCKET_X, CardStandMenu.POCKET_Y, CardStandMenu.POCKET_WIDTH, CardStandMenu.POCKET_HEIGHT, mouseX, mouseY);
        }
        return super.isHovering(x, y, width, height, mouseX, mouseY);
    }

    protected void pressButton(int button) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player != null && minecraft.gameMode != null && menu.clickMenuButton(minecraft.player, button)) {
            minecraft.gameMode.handleInventoryButtonClick(menu.containerId, button);
        }
    }

    protected void drawCentered(GuiGraphics graphics, Component text, int centerX, int y, int color) {
        graphics.drawString(font, text, centerX - font.width(text) / 2, y, color, false);
    }

    protected Component trimmed(Component text, int width) {
        if (font.width(text) <= width) {
            return text;
        }
        return Component.literal(font.plainSubstrByWidth(text.getString(), width - font.width("…")) + "…").withStyle(text.getStyle());
    }
}
