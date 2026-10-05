package com.coolerpromc.cobblemontcg.menu;

import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.TcgCardData;
import com.coolerpromc.cobblemontcg.item.custom.CardBinderItem;
import com.coolerpromc.cobblemontcg.item.custom.TcgCardItem;
import net.minecraft.core.NonNullList;
import net.minecraft.core.component.DataComponents;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.AbstractContainerMenu;
import net.minecraft.world.inventory.ClickType;
import net.minecraft.world.inventory.DataSlot;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemContainerContents;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class CardBinderMenu extends AbstractContainerMenu {
    public static final int PAGE_SLOTS = 9;
    public static final int PAGES = 24;
    public static final int SPREAD_SLOTS = PAGE_SLOTS * 2;
    public static final int SPREADS = PAGES / 2;
    public static final int CAPACITY = PAGE_SLOTS * PAGES;

    public static final int BUTTON_PREVIOUS = 0;
    public static final int BUTTON_NEXT = 1;
    public static final int BUTTON_SORT = 2;

    public static final int POCKET_WIDTH = 22;
    public static final int POCKET_HEIGHT = 30;
    public static final int[] POCKET_X = {13, 39, 65, 113, 139, 165};
    public static final int[] POCKET_Y = {12, 45, 78};
    public static final int INVENTORY_X = 20;
    public static final int INVENTORY_Y = 148;
    public static final int HOTBAR_Y = 206;

    private static final int INVENTORY_START = SPREAD_SLOTS;
    private static final int HOTBAR_START = INVENTORY_START + 27;
    private static final int SLOTS_END = HOTBAR_START + 9;

    private final SimpleContainer cards;
    private final SpreadView view;
    private final DataSlot binderSlot = DataSlot.standalone();
    private final ItemStack binder;
    private int spread;
    private boolean suspendSave;

    public CardBinderMenu(int containerId, Inventory inventory) {
        this(containerId, inventory, -1, ItemStack.EMPTY);
    }

    public CardBinderMenu(int containerId, Inventory inventory, int binderSlot, ItemStack binder) {
        super(ModMenuTypes.CARD_BINDER.get(), containerId);
        this.binder = binder;
        this.binderSlot.set(binderSlot);
        this.cards = new SimpleContainer(CAPACITY);
        this.view = new SpreadView();

        if (!binder.isEmpty()) {
            NonNullList<ItemStack> items = NonNullList.withSize(CAPACITY, ItemStack.EMPTY);
            binder.getOrDefault(DataComponents.CONTAINER, ItemContainerContents.EMPTY).copyInto(items);
            for (int i = 0; i < CAPACITY; i++) {
                this.cards.setItem(i, items.get(i));
            }
            this.cards.addListener(container -> save());
        }

        for (int i = 0; i < SPREAD_SLOTS; i++) {
            int page = i / PAGE_SLOTS;
            int pocket = i % PAGE_SLOTS;
            addSlot(new PocketSlot(this.view, i, POCKET_X[page * 3 + pocket % 3] + (POCKET_WIDTH - 16) / 2, POCKET_Y[pocket / 3] + (POCKET_HEIGHT - 16) / 2));
        }
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 9; col++) {
                addSlot(new InventorySlot(inventory, col + row * 9 + 9, INVENTORY_X + col * 18, INVENTORY_Y + row * 18));
            }
        }
        for (int col = 0; col < 9; col++) {
            addSlot(new InventorySlot(inventory, col, INVENTORY_X + col * 18, HOTBAR_Y));
        }
        addDataSlot(this.binderSlot);
    }

    public static boolean isCard(ItemStack stack) {
        return stack.getItem() instanceof TcgCardItem;
    }

    public int spread() {
        return spread;
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        switch (id) {
            case BUTTON_PREVIOUS -> {
                if (spread <= 0) {
                    return false;
                }
                spread--;
            }
            case BUTTON_NEXT -> {
                if (spread >= SPREADS - 1) {
                    return false;
                }
                spread++;
            }
            case BUTTON_SORT -> {
                if (player.level().isClientSide()) {
                    return true;
                }
                sort();
            }
            default -> {
                return false;
            }
        }
        if (!player.level().isClientSide()) {
            sendAllDataToRemote();
        }
        return true;
    }

    private void sort() {
        List<ItemStack> merged = new ArrayList<>();
        for (int i = 0; i < CAPACITY; i++) {
            ItemStack stack = cards.getItem(i);
            if (stack.isEmpty()) {
                continue;
            }
            ItemStack target = merged.stream().filter(s -> ItemStack.isSameItemSameComponents(s, stack)).findFirst().orElse(null);
            if (target == null) {
                merged.add(stack.copy());
            } else {
                target.grow(stack.getCount());
            }
        }
        merged.sort(CARD_ORDER);

        List<ItemStack> sorted = new ArrayList<>();
        for (ItemStack stack : merged) {
            while (!stack.isEmpty()) {
                sorted.add(stack.split(stack.getMaxStackSize()));
            }
        }
        suspendSave = true;
        for (int i = 0; i < CAPACITY; i++) {
            cards.setItem(i, i < sorted.size() ? sorted.get(i) : ItemStack.EMPTY);
        }
        suspendSave = false;
        save();
    }

    private static final Comparator<ItemStack> CARD_ORDER = Comparator.comparing(
            (ItemStack stack) -> stack.get(ModDataComponents.TCG_CARD.get()),
            Comparator.nullsLast(Comparator.comparing((TcgCardData data) -> data.setId().toString())
                    .thenComparingInt(TcgCardData::cardNumber)
                    .thenComparing(TcgCardData::holo)));

    private void save() {
        if (binder.isEmpty() || suspendSave) {
            return;
        }
        List<ItemStack> items = new ArrayList<>(CAPACITY);
        for (int i = 0; i < CAPACITY; i++) {
            items.add(cards.getItem(i).copy());
        }
        binder.set(DataComponents.CONTAINER, ItemContainerContents.fromItems(items));
    }

    private ItemStack insert(ItemStack stack) {
        for (int i = 0; i < CAPACITY && !stack.isEmpty(); i++) {
            ItemStack existing = cards.getItem(i);
            if (!existing.isEmpty() && ItemStack.isSameItemSameComponents(existing, stack)) {
                int moved = Math.min(stack.getCount(), existing.getMaxStackSize() - existing.getCount());
                if (moved > 0) {
                    existing.grow(moved);
                    stack.shrink(moved);
                    cards.setChanged();
                }
            }
        }
        for (int n = 0; n < CAPACITY && !stack.isEmpty(); n++) {
            int i = (spread * SPREAD_SLOTS + n) % CAPACITY;
            if (cards.getItem(i).isEmpty()) {
                cards.setItem(i, stack.split(stack.getMaxStackSize()));
            }
        }
        return stack;
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = slots.get(index);
        if (!slot.hasItem() || !slot.mayPickup(player)) {
            return ItemStack.EMPTY;
        }
        ItemStack stack = slot.getItem();
        if (index < SPREAD_SLOTS) {
            if (!moveItemStackTo(stack, INVENTORY_START, SLOTS_END, true)) {
                return ItemStack.EMPTY;
            }
        } else if (isCard(stack)) {
            if (player.level().isClientSide()) {
                return ItemStack.EMPTY;
            }
            insert(stack);
        } else if (index < HOTBAR_START) {
            if (!moveItemStackTo(stack, HOTBAR_START, SLOTS_END, false)) {
                return ItemStack.EMPTY;
            }
        } else if (!moveItemStackTo(stack, INVENTORY_START, HOTBAR_START, false)) {
            return ItemStack.EMPTY;
        }
        if (stack.isEmpty()) {
            slot.setByPlayer(ItemStack.EMPTY);
        } else {
            slot.setChanged();
        }
        return ItemStack.EMPTY;
    }

    @Override
    public void clicked(int slotId, int button, ClickType clickType, Player player) {
        // number keys and the offhand key would swap the open binder out of its slot
        if (clickType == ClickType.SWAP && button == binderSlot.get()) {
            return;
        }
        super.clicked(slotId, button, clickType, player);
    }

    @Override
    public boolean stillValid(Player player) {
        if (binder.isEmpty()) {
            return true;
        }
        int slot = binderSlot.get();
        return player.isAlive() && slot >= 0 && player.getInventory().getItem(slot) == binder && binder.getItem() instanceof CardBinderItem;
    }

    private class SpreadView implements Container {
        private int index(int slot) {
            return spread * SPREAD_SLOTS + slot;
        }

        @Override
        public int getContainerSize() {
            return SPREAD_SLOTS;
        }

        @Override
        public boolean isEmpty() {
            for (int i = 0; i < SPREAD_SLOTS; i++) {
                if (!getItem(i).isEmpty()) {
                    return false;
                }
            }
            return true;
        }

        @Override
        public ItemStack getItem(int slot) {
            return cards.getItem(index(slot));
        }

        @Override
        public ItemStack removeItem(int slot, int amount) {
            return cards.removeItem(index(slot), amount);
        }

        @Override
        public ItemStack removeItemNoUpdate(int slot) {
            return cards.removeItemNoUpdate(index(slot));
        }

        @Override
        public void setItem(int slot, ItemStack stack) {
            cards.setItem(index(slot), stack);
        }

        @Override
        public void setChanged() {
            cards.setChanged();
        }

        @Override
        public boolean stillValid(Player player) {
            return true;
        }

        @Override
        public boolean canPlaceItem(int slot, ItemStack stack) {
            return isCard(stack);
        }

        @Override
        public void clearContent() {
            for (int i = 0; i < SPREAD_SLOTS; i++) {
                setItem(i, ItemStack.EMPTY);
            }
        }
    }

    public static class PocketSlot extends Slot {
        public PocketSlot(Container container, int slot, int x, int y) {
            super(container, slot, x, y);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return isCard(stack);
        }

        @Override
        public boolean isHighlightable() {
            return false;
        }
    }

    private class InventorySlot extends Slot {
        InventorySlot(Container container, int slot, int x, int y) {
            super(container, slot, x, y);
        }

        private boolean isBinder() {
            return getContainerSlot() == binderSlot.get();
        }

        @Override
        public boolean mayPickup(Player player) {
            return !isBinder() && super.mayPickup(player);
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return !isBinder() && super.mayPlace(stack);
        }
    }
}
