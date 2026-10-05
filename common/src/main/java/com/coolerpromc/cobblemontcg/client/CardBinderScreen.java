package com.coolerpromc.cobblemontcg.client;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardBinderMenu;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.AbstractContainerScreen;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import org.lwjgl.glfw.GLFW;

public class CardBinderScreen extends AbstractContainerScreen<CardBinderMenu> {
    private static final ResourceLocation TEXTURE = Constants.id("textures/gui/card_binder.png");
    private static final String KEY = "screen." + Constants.MODID + ".card_binder.";
    private static final float CARD_SCALE = 1.75F;

    private static final int ARROW_W = 12;
    private static final int ARROW_H = 10;
    private static final int PREVIOUS_X = 9;
    private static final int NEXT_X = 179;
    private static final int ARROW_Y = 111;
    private static final int SORT_X = 172;
    private static final int SORT_Y = 133;
    private static final int SORT_SIZE = 12;
    private static final int PAGE_LABEL_Y = 112;
    private static final int[] PAGE_CENTER_X = {50, 150};

    public CardBinderScreen(CardBinderMenu menu, Inventory inventory, Component title) {
        super(menu, inventory, title);
        this.imageWidth = 200;
        this.imageHeight = 228;
        this.inventoryLabelX = CardBinderMenu.INVENTORY_X;
        this.inventoryLabelY = 136;
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        double[] mouse = toSlot(mouseX, mouseY);
        super.render(graphics, (int) mouse[0], (int) mouse[1], partialTick);
        renderTooltip(graphics, (int) mouse[0], (int) mouse[1]);
        if (isOver(SORT_X, SORT_Y, SORT_SIZE, SORT_SIZE, mouseX, mouseY)) {
            graphics.renderTooltip(font, Component.translatable(KEY + "sort"), mouseX, mouseY);
        }
    }

    @Override
    protected void renderBg(GuiGraphics graphics, float partialTick, int mouseX, int mouseY) {
        graphics.blit(TEXTURE, leftPos, topPos, 0, 0, imageWidth, imageHeight);
        int spread = menu.spread();
        arrow(graphics, PREVIOUS_X, 0, spread > 0, mouseX, mouseY);
        arrow(graphics, NEXT_X, ARROW_H, spread < CardBinderMenu.SPREADS - 1, mouseX, mouseY);
        boolean sortHovered = isOver(SORT_X, SORT_Y, SORT_SIZE, SORT_SIZE, mouseX, mouseY);
        graphics.blit(TEXTURE, leftPos + SORT_X, topPos + SORT_Y, sortHovered ? 212 : 200, 20, SORT_SIZE, SORT_SIZE);
    }

    private void arrow(GuiGraphics graphics, int x, int v, boolean enabled, int mouseX, int mouseY) {
        int u = !enabled ? 224 : isOver(x, ARROW_Y, ARROW_W, ARROW_H, mouseX, mouseY) ? 212 : 200;
        graphics.blit(TEXTURE, leftPos + x, topPos + ARROW_Y, u, v, ARROW_W, ARROW_H);
    }

    @Override
    protected void renderLabels(GuiGraphics graphics, int mouseX, int mouseY) {
        graphics.drawString(font, playerInventoryTitle, inventoryLabelX, inventoryLabelY, 0x404040, false);
        for (int page = 0; page < 2; page++) {
            Component label = Component.translatable(KEY + "page", menu.spread() * 2 + page + 1, CardBinderMenu.PAGES);
            graphics.drawString(font, label, PAGE_CENTER_X[page] - font.width(label) / 2, PAGE_LABEL_Y, 0x8A8270, false);
        }
        if (hoveredSlot instanceof CardBinderMenu.PocketSlot slot) {
            int x = slot.x - (CardBinderMenu.POCKET_WIDTH - 16) / 2;
            int y = slot.y - (CardBinderMenu.POCKET_HEIGHT - 16) / 2;
            graphics.fill(RenderType.guiOverlay(), x + 1, y + 1, x + CardBinderMenu.POCKET_WIDTH - 1, y + CardBinderMenu.POCKET_HEIGHT - 1, 0x60FFFFFF);
        }
    }

    @Override
    protected void renderSlot(GuiGraphics graphics, Slot slot) {
        if (!(slot instanceof CardBinderMenu.PocketSlot)) {
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
        graphics.renderItemDecorations(font, stack, slot.x + 1, slot.y + 5);
    }

    private double[] toSlot(double mouseX, double mouseY) {
        for (Slot slot : menu.slots) {
            if (slot instanceof CardBinderMenu.PocketSlot) {
                int x = leftPos + slot.x - (CardBinderMenu.POCKET_WIDTH - 16) / 2;
                int y = topPos + slot.y - (CardBinderMenu.POCKET_HEIGHT - 16) / 2;
                if (mouseX >= x && mouseX < x + CardBinderMenu.POCKET_WIDTH && mouseY >= y && mouseY < y + CardBinderMenu.POCKET_HEIGHT) {
                    return new double[]{leftPos + slot.x + 8, topPos + slot.y + 8};
                }
            }
        }
        return new double[]{mouseX, mouseY};
    }

    private boolean isOver(int x, int y, int w, int h, double mouseX, double mouseY) {
        return mouseX >= leftPos + x && mouseX < leftPos + x + w && mouseY >= topPos + y && mouseY < topPos + y + h;
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == GLFW.GLFW_MOUSE_BUTTON_LEFT) {
            if (isOver(PREVIOUS_X, ARROW_Y, ARROW_W, ARROW_H, mouseX, mouseY)) {
                return press(CardBinderMenu.BUTTON_PREVIOUS);
            }
            if (isOver(NEXT_X, ARROW_Y, ARROW_W, ARROW_H, mouseX, mouseY)) {
                return press(CardBinderMenu.BUTTON_NEXT);
            }
            if (isOver(SORT_X, SORT_Y, SORT_SIZE, SORT_SIZE, mouseX, mouseY)) {
                return press(CardBinderMenu.BUTTON_SORT);
            }
        }
        double[] mouse = toSlot(mouseX, mouseY);
        return super.mouseClicked(mouse[0], mouse[1], button);
    }

    @Override
    public boolean mouseReleased(double mouseX, double mouseY, int button) {
        double[] mouse = toSlot(mouseX, mouseY);
        return super.mouseReleased(mouse[0], mouse[1], button);
    }

    @Override
    public boolean mouseDragged(double mouseX, double mouseY, int button, double dragX, double dragY) {
        double[] mouse = toSlot(mouseX, mouseY);
        return super.mouseDragged(mouse[0], mouse[1], button, dragX, dragY);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        if (scrollY != 0 && mouseY < topPos + 128) {
            press(scrollY > 0 ? CardBinderMenu.BUTTON_PREVIOUS : CardBinderMenu.BUTTON_NEXT);
            return true;
        }
        return super.mouseScrolled(mouseX, mouseY, scrollX, scrollY);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_LEFT || keyCode == GLFW.GLFW_KEY_PAGE_UP) {
            press(CardBinderMenu.BUTTON_PREVIOUS);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_RIGHT || keyCode == GLFW.GLFW_KEY_PAGE_DOWN) {
            press(CardBinderMenu.BUTTON_NEXT);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    private boolean press(int button) {
        Minecraft minecraft = Minecraft.getInstance();
        if (minecraft.player == null || minecraft.gameMode == null || !menu.clickMenuButton(minecraft.player, button)) {
            return false;
        }
        minecraft.gameMode.handleInventoryButtonClick(menu.containerId, button);
        minecraft.getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1.0F));
        return true;
    }
}
