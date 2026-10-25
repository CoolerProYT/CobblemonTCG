package com.coolerpromc.cobblemontcg.menu;

import net.minecraft.world.Container;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.MenuType;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntity;
import org.jetbrains.annotations.Nullable;

public abstract class CardStandMenu extends AbstractContainerMenu {
    public static final int POCKET_X = 14;
    public static final int POCKET_Y = 18;
    public static final int POCKET_WIDTH = 36;
    public static final int POCKET_HEIGHT = 50;
    public static final int CARD_X = POCKET_X + (POCKET_WIDTH - 16) / 2;
    public static final int CARD_Y = POCKET_Y + (POCKET_HEIGHT - 16) / 2;
    public static final int INVENTORY_X = 8;
    public static final int INVENTORY_Y = 120;
    public static final int HOTBAR_Y = 178;

    protected CardStandMenu(@Nullable MenuType<?> menuType, int containerId) {
        super(menuType, containerId);
    }

    protected abstract int standSlots();

    protected void addPlayerInventory(Inventory inventory) {
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                addSlot(new Slot(inventory, col + row * 9 + 9, INVENTORY_X + col * 18, INVENTORY_Y + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            addSlot(new Slot(inventory, col, INVENTORY_X + col * 18, HOTBAR_Y));
        }
    }

    protected static int readInt(ContainerData data, int index) {
        return (data.get(index) & 0xFFFF) | (data.get(index + 1) & 0xFFFF) << 16;
    }

    protected static boolean stillValid(BlockEntity stand, Player player) {
        return !stand.isRemoved() && player.level().getBlockEntity(stand.getBlockPos()) == stand
                && player.distanceToSqr(stand.getBlockPos().getCenter()) <= 64.0;
    }

    @Override
    public boolean canTakeItemForPickAll(ItemStack stack, Slot slot) {
        return !(slot instanceof DisplaySlot) && super.canTakeItemForPickAll(stack, slot);
    }

    public static class CardSlot extends Slot {
        public CardSlot(Container container, int slot, int x, int y) {
            super(container, slot, x, y);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return CardBinderMenu.isCard(stack);
        }

        @Override
        public boolean isHighlightable() {
            return false;
        }
    }

    public static class DisplaySlot extends Slot {
        public DisplaySlot(Container container, int slot, int x, int y) {
            super(container, slot, x, y);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return false;
        }

        @Override
        public boolean mayPickup(Player player) {
            return false;
        }
    }
}
