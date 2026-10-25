package com.coolerpromc.cobblemontcg.block.entity;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.menu.CardBinderMenu;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.NonNullList;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.protocol.game.ClientboundBlockEntityDataPacket;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Containers;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class CardDisplayStandBlockEntity extends BlockEntity {
    public static final int MAX_PRICE = 9999;
    private static final String MESSAGE = "message." + Constants.MODID + ".card_display_stand.";

    private @Nullable UUID owner;
    private String ownerName = "";
    private final SimpleContainer stock = new SimpleContainer(1);
    private final SimpleContainer price = new SimpleContainer(1);
    private int priceAmount = 1;
    private final List<TillEntry> till = new ArrayList<>();

    public record TillEntry(ItemStack item, int count) {
    }

    public enum Purchase {
        BOUGHT, SOLD_OUT, NOT_FOR_SALE, CANNOT_AFFORD, OWN_STAND
    }

    public CardDisplayStandBlockEntity(BlockPos pos, BlockState state) {
        super(ModBlockEntities.CARD_DISPLAY_STAND.get(), pos, state);
        stock.addListener(container -> changed());
        price.addListener(container -> changed());
    }

    public SimpleContainer stock() {
        return stock;
    }

    public SimpleContainer price() {
        return price;
    }

    public ItemStack card() {
        return stock.getItem(0);
    }

    public ItemStack priceItem() {
        return price.getItem(0);
    }

    public int priceAmount() {
        return priceAmount;
    }

    public String ownerName() {
        return ownerName;
    }

    public boolean isForSale() {
        return !card().isEmpty() && !priceItem().isEmpty();
    }

    public boolean hasOwner() {
        return owner != null;
    }

    public boolean isOwner(Player player) {
        return owner == null || owner.equals(player.getUUID());
    }

    public boolean canBreak(Player player) {
        return isOwner(player) || (player.isCreative() && player.hasPermissions(2));
    }

    public void setOwner(Player player) {
        owner = player.getUUID();
        ownerName = player.getGameProfile().getName();
        changed();
    }

    public void setPriceItem(ItemStack item) {
        price.setItem(0, item.copyWithCount(1));
    }

    public void setPriceAmount(int amount) {
        int clamped = Math.clamp(amount, 1, MAX_PRICE);
        if (clamped != priceAmount) {
            priceAmount = clamped;
            changed();
        }
    }

    public boolean placeCard(ItemStack held) {
        ItemStack shown = card();
        if (!CardBinderMenu.isCard(held)) {
            return false;
        }
        if (shown.isEmpty()) {
            stock.setItem(0, held.split(1));
            return true;
        }
        if (ItemStack.isSameItemSameComponents(shown, held) && shown.getCount() < shown.getMaxStackSize()) {
            shown.grow(1);
            held.shrink(1);
            stock.setChanged();
            return true;
        }
        return false;
    }

    public boolean takeCard(Player player) {
        ItemStack shown = stock.removeItemNoUpdate(0);
        if (shown.isEmpty()) {
            return false;
        }
        stock.setChanged();
        player.getInventory().placeItemBackInInventory(shown);
        return true;
    }

    public static boolean pays(ItemStack stack, ItemStack priceItem) {
        return !stack.isEmpty() && ItemStack.isSameItemSameComponents(stack, priceItem);
    }

    public static int countPayment(Inventory inventory, ItemStack priceItem) {
        if (priceItem.isEmpty()) {
            return 0;
        }
        int total = 0;
        for (NonNullList<ItemStack> list : List.of(inventory.items, inventory.offhand)) {
            for (ItemStack stack : list) {
                if (pays(stack, priceItem)) {
                    total += stack.getCount();
                }
            }
        }
        return total;
    }

    public Purchase buy(ServerPlayer buyer) {
        if (owner != null && owner.equals(buyer.getUUID())) {
            return Purchase.OWN_STAND;
        }
        if (priceItem().isEmpty()) {
            return Purchase.NOT_FOR_SALE;
        }
        if (card().isEmpty()) {
            return Purchase.SOLD_OUT;
        }
        ItemStack priceItem = priceItem().copy();
        int amount = priceAmount;
        Inventory inventory = buyer.getInventory();
        if (countPayment(inventory, priceItem) < amount) {
            return Purchase.CANNOT_AFFORD;
        }

        int left = amount;
        for (NonNullList<ItemStack> list : List.of(inventory.offhand, inventory.items)) {
            for (int i = list.size() - 1; i >= 0 && left > 0; i--) {
                ItemStack stack = list.get(i);
                if (pays(stack, priceItem)) {
                    int taken = Math.min(left, stack.getCount());
                    stack.shrink(taken);
                    left -= taken;
                }
            }
        }
        inventory.setChanged();
        addToTill(priceItem, amount);

        ItemStack card = stock.removeItem(0, 1);
        Component cardName = card.getHoverName();
        inventory.placeItemBackInInventory(card);

        if (level != null) {
            level.playSound(null, worldPosition, SoundEvents.VILLAGER_YES, SoundSource.BLOCKS, 0.6F, 1.2F);
            level.playSound(null, worldPosition, SoundEvents.EXPERIENCE_ORB_PICKUP, SoundSource.BLOCKS, 0.5F, 1.0F);
            if (owner != null && level.getServer() != null) {
                ServerPlayer seller = level.getServer().getPlayerList().getPlayer(owner);
                if (seller != null) {
                    seller.sendSystemMessage(Component.translatable(MESSAGE + "sold", buyer.getDisplayName(), cardName, amount, priceItem.getHoverName()));
                }
            }
        }
        return Purchase.BOUGHT;
    }

    private void addToTill(ItemStack item, int count) {
        for (int i = 0; i < till.size(); i++) {
            TillEntry entry = till.get(i);
            if (ItemStack.isSameItemSameComponents(entry.item(), item)) {
                till.set(i, new TillEntry(entry.item(), (int) Math.min(Integer.MAX_VALUE, (long) entry.count() + count)));
                changed();
                return;
            }
        }
        till.add(new TillEntry(item.copyWithCount(1), count));
        changed();
    }

    public List<TillEntry> till() {
        return till;
    }

    public int tillTotal() {
        long total = 0;
        for (TillEntry entry : till) {
            total += entry.count();
        }
        return (int) Math.min(Integer.MAX_VALUE, total);
    }

    public boolean collectTill(Player player) {
        if (till.isEmpty()) {
            return false;
        }
        for (ItemStack stack : tillStacks()) {
            player.getInventory().placeItemBackInInventory(stack);
        }
        till.clear();
        changed();
        return true;
    }

    private List<ItemStack> tillStacks() {
        List<ItemStack> stacks = new ArrayList<>();
        for (TillEntry entry : till) {
            int left = entry.count();
            int max = entry.item().getMaxStackSize();
            while (left > 0) {
                int count = Math.min(left, max);
                stacks.add(entry.item().copyWithCount(count));
                left -= count;
            }
        }
        return stacks;
    }

    public void dropContents(Level level, BlockPos pos) {
        Containers.dropItemStack(level, pos.getX(), pos.getY(), pos.getZ(), stock.removeItemNoUpdate(0));
        for (ItemStack stack : tillStacks()) {
            Containers.dropItemStack(level, pos.getX(), pos.getY(), pos.getZ(), stack);
        }
        till.clear();
    }

    private void changed() {
        if (level == null || level.isClientSide()) {
            return;
        }
        setChanged();
        BlockState state = getBlockState();
        level.sendBlockUpdated(worldPosition, state, state, Block.UPDATE_CLIENTS);
    }

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        writeShown(tag, registries);
        ListTag entries = new ListTag();
        for (TillEntry entry : till) {
            CompoundTag entryTag = new CompoundTag();
            entryTag.put("item", entry.item().save(registries));
            entryTag.putInt("count", entry.count());
            entries.add(entryTag);
        }
        tag.put("till", entries);
    }

    private void writeShown(CompoundTag tag, HolderLookup.Provider registries) {
        if (owner != null) {
            tag.putUUID("owner", owner);
        }
        tag.putString("owner_name", ownerName);
        if (!card().isEmpty()) {
            tag.put("card", card().save(registries));
        }
        if (!priceItem().isEmpty()) {
            tag.put("price", priceItem().save(registries));
        }
        tag.putInt("price_amount", priceAmount);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        owner = tag.hasUUID("owner") ? tag.getUUID("owner") : null;
        ownerName = tag.getString("owner_name");
        stock.setItem(0, ItemStack.parseOptional(registries, tag.getCompound("card")));
        price.setItem(0, ItemStack.parseOptional(registries, tag.getCompound("price")));
        priceAmount = tag.contains("price_amount") ? Math.clamp(tag.getInt("price_amount"), 1, MAX_PRICE) : 1;
        till.clear();
        for (Tag element : tag.getList("till", Tag.TAG_COMPOUND)) {
            CompoundTag entryTag = (CompoundTag) element;
            ItemStack item = ItemStack.parseOptional(registries, entryTag.getCompound("item"));
            int count = entryTag.getInt("count");
            if (!item.isEmpty() && count > 0) {
                till.add(new TillEntry(item, count));
            }
        }
    }

    @Override
    public CompoundTag getUpdateTag(HolderLookup.Provider registries) {
        CompoundTag tag = new CompoundTag();
        writeShown(tag, registries);
        return tag;
    }

    @Override
    public @Nullable Packet<ClientGamePacketListener> getUpdatePacket() {
        return ClientboundBlockEntityDataPacket.create(this);
    }
}
