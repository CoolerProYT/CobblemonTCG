package com.coolerpromc.cobblemontcg.menu;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.Container;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.ClickType;
import net.minecraft.world.inventory.ContainerData;
import net.minecraft.world.inventory.SimpleContainerData;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

public class CardStandBuyerMenu extends CardStandMenu {
    public static final int CARD_SLOT = 0;
    public static final int PRICE_SLOT = 1;
    public static final int BUTTON_BUY = 0;

    public static final int PRICE_X = 60;
    public static final int PRICE_Y = 62;

    private static final String MESSAGE = "message." + Constants.MODID + ".card_display_stand.";

    private final @Nullable CardDisplayStandBlockEntity stand;
    private final Inventory inventory;
    private final ContainerData data;

    public CardStandBuyerMenu(int containerId, Inventory inventory) {
        this(containerId, inventory, null, new SimpleContainer(1), new SimpleContainer(1), new SimpleContainerData(2));
    }

    public CardStandBuyerMenu(int containerId, Inventory inventory, CardDisplayStandBlockEntity stand) {
        this(containerId, inventory, stand, stand.stock(), stand.price(), new AmountData(stand));
    }

    private CardStandBuyerMenu(int containerId, Inventory inventory, @Nullable CardDisplayStandBlockEntity stand, Container stock, Container price, ContainerData data) {
        super(ModMenuTypes.CARD_STAND_BUYER.get(), containerId);
        this.stand = stand;
        this.inventory = inventory;
        this.data = data;
        addSlot(new DisplaySlot(stock, 0, CARD_X, CARD_Y));
        addSlot(new DisplaySlot(price, 0, PRICE_X, PRICE_Y));
        addPlayerInventory(inventory);
        addDataSlots(data);
    }

    @Override
    protected int standSlots() {
        return 2;
    }

    public ItemStack card() {
        return slots.get(CARD_SLOT).getItem();
    }

    public ItemStack priceItem() {
        return slots.get(PRICE_SLOT).getItem();
    }

    public int priceAmount() {
        return Math.max(1, readInt(data, 0));
    }

    public int payment() {
        return CardDisplayStandBlockEntity.countPayment(inventory, priceItem());
    }

    @Override
    public boolean clickMenuButton(Player player, int id) {
        if (id != BUTTON_BUY) {
            return false;
        }
        if (stand != null && player instanceof ServerPlayer buyer) {
            CardDisplayStandBlockEntity.Purchase result = stand.buy(buyer);
            if (result != CardDisplayStandBlockEntity.Purchase.BOUGHT) {
                buyer.displayClientMessage(Component.translatable(MESSAGE + result.name().toLowerCase()), true);
            }
            broadcastChanges();
        }
        return true;
    }

    @Override
    public void clicked(int slotId, int button, ClickType clickType, Player player) {
        if (slotId == CARD_SLOT || slotId == PRICE_SLOT) {
            return;
        }
        super.clicked(slotId, button, clickType, player);
    }

    @Override
    public ItemStack quickMoveStack(Player player, int index) {
        return ItemStack.EMPTY;
    }

    @Override
    public boolean stillValid(Player player) {
        return stand == null || stillValid(stand, player);
    }

    private record AmountData(CardDisplayStandBlockEntity stand) implements ContainerData {
        @Override
        public int get(int index) {
            return index == 0 ? stand.priceAmount() & 0xFFFF : stand.priceAmount() >>> 16;
        }

        @Override
        public void set(int index, int value) {
        }

        @Override
        public int getCount() {
            return 2;
        }
    }
}
