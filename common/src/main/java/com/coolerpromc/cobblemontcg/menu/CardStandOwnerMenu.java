package com.coolerpromc.cobblemontcg.menu;

import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ClickType;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

public class CardStandOwnerMenu extends CardStandMenu {
    public static final int CARD_SLOT = 0;
    public static final int PRICE_SLOT = 1;
    public static final int TILL_SLOT = 2;

    public static final int BUTTON_COLLECT = 0;
    public static final int BUTTON_CLEAR_PRICE = 1;
    public static final int BUTTON_AMOUNT = 100;

    public static final int PRICE_X = 60;
    public static final int PRICE_Y = 32;
    public static final int TILL_X = 60;
    public static final int TILL_Y = 76;

    private static final int DATA_AMOUNT = 0;
    private static final int DATA_TILL_TOTAL = 2;
    private static final int DATA_TILL_KINDS = 4;

    private final @Nullable CardDisplayStandBlockEntity stand;
    private final ContainerData data;

    public CardStandOwnerMenu(int containerId, Inventory inventory) {
        this(containerId, inventory, null, new SimpleContainer(1), new SimpleContainer(1), new SimpleContainer(1), new SimpleContainerData(5));
    }

    public CardStandOwnerMenu(int containerId, Inventory inventory, CardDisplayStandBlockEntity stand) {
        this(containerId, inventory, stand, stand.stock(), stand.price(), new TillView(stand), new StandData(stand));
    }

    private CardStandOwnerMenu(int containerId, Inventory inventory, @Nullable CardDisplayStandBlockEntity stand, Container stock, Container price, Container till, ContainerData data) {
        super(ModMenuTypes.CARD_STAND_OWNER.get(), containerId);
        this.stand = stand;
        this.data = data;
        addSlot(new CardSlot(stock, 0, CARD_X, CARD_Y));
        addSlot(new DisplaySlot(price, 0, PRICE_X, PRICE_Y));
        addSlot(new DisplaySlot(till, 0, TILL_X, TILL_Y));
        addPlayerInventory(inventory);
        addDataSlots(data);
    }

    @Override
    protected int standSlots() {
        return 3;
    }

    public int priceAmount() {
        return Math.max(1, readInt(data, DATA_AMOUNT));
    }

    public int tillTotal() {
        return readInt(data, DATA_TILL_TOTAL);
    }

    public int tillKinds() {
        return data.get(DATA_TILL_KINDS);
    }

    public void setPriceItem(ItemStack item) {
        if (stand != null) {
            stand.setPriceItem(item);
        }
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (id >= BUTTON_AMOUNT) {
            int amount = id - BUTTON_AMOUNT;
            if (amount < 1 || amount > CardDisplayStandBlockEntity.MAX_PRICE) {
                return false;
            }
            if (stand != null) {
                stand.setPriceAmount(amount);
            }
            return true;
        }
        return switch (id) {
            case BUTTON_COLLECT -> stand == null || stand.collectTill(player);
            case BUTTON_CLEAR_PRICE -> {
                if (stand != null) {
                    stand.setPriceItem(ItemStack.EMPTY);
                }
                yield true;
            }
            default -> false;
        };
    }

    @Override
    public void clicked(int slotId, int button, ClickType clickType, Player player) {
        if (slotId == PRICE_SLOT) {
            if ((clickType == ClickType.PICKUP || clickType == ClickType.QUICK_MOVE) && stand != null) {
                stand.setPriceItem(getCarried());
            }
            return;
        }
        if (slotId == TILL_SLOT) {
            return;
        }
        super.clicked(slotId, button, clickType, player);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        Slot slot = slots.get(index);
        if (!slot.hasItem()) {
            return ItemStack.EMPTY;
        }
        ItemStack stack = slot.getItem();
        if (index == CARD_SLOT) {
            if (!moveItemStackTo(stack, standSlots(), slots.size(), true)) {
                return ItemStack.EMPTY;
            }
        } else if (index >= standSlots()) {
            if (CardBinderMenu.isCard(stack) && slots.get(CARD_SLOT).mayPlace(stack)) {
                if (!moveItemStackTo(stack, CARD_SLOT, CARD_SLOT + 1, false)) {
                    return ItemStack.EMPTY;
                }
            } else {
                if (stand != null) {
                    stand.setPriceItem(stack);
                }
                return ItemStack.EMPTY;
            }
        } else {
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
    public boolean stillValid(Player player) {
        return stand == null || (stillValid(stand, player) && stand.isOwner(player));
    }

    private static class TillView extends SimpleContainer {
        private final CardDisplayStandBlockEntity stand;

        TillView(CardDisplayStandBlockEntity stand) {
            super(1);
            this.stand = stand;
        }

        @Override
        public ItemStack getItem(int slot) {
            return stand.till().isEmpty() ? ItemStack.EMPTY : stand.till().getFirst().item();
        }
    }

    private record StandData(CardDisplayStandBlockEntity stand) implements ContainerData {
        @Override
        public int get(int index) {
            return switch (index) {
                case DATA_AMOUNT -> stand.priceAmount() & 0xFFFF;
                case DATA_AMOUNT + 1 -> stand.priceAmount() >>> 16;
                case DATA_TILL_TOTAL -> stand.tillTotal() & 0xFFFF;
                case DATA_TILL_TOTAL + 1 -> stand.tillTotal() >>> 16;
                case DATA_TILL_KINDS -> stand.till().size();
                default -> 0;
            };
        }

        @Override
        public void set(int index, int value) {
        }

        @Override
        public int getCount() {
            return 5;
        }
    }
}
