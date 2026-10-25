package com.coolerpromc.cobblemontcg.gametest;

import com.coolerpromc.cobblemontcg.Constants;
import com.coolerpromc.cobblemontcg.block.ModBlocks;
import com.coolerpromc.cobblemontcg.block.entity.CardDisplayStandBlockEntity;
import com.coolerpromc.cobblemontcg.component.ModDataComponents;
import com.coolerpromc.cobblemontcg.component.custom.TcgCardData;
import com.coolerpromc.cobblemontcg.item.ModItems;
import com.coolerpromc.cobblemontcg.menu.CardStandBuyerMenu;
import com.coolerpromc.cobblemontcg.menu.CardStandOwnerMenu;
import io.netty.buffer.Unpooled;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.network.protocol.game.ServerboundContainerButtonClickPacket;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.inventory.ClickType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

@GameTestHolder(Constants.MODID)
@PrefixGameTestTemplate(false)
public class CardDisplayStandGameTests {
    private static final String EMPTY = "empty";
    private static final int OFFHAND_SLOT = 40;

    @GameTest(template = EMPTY)
    public static void ownerStocksAndPricesTheStand(GameTestHelper helper) {
        ServerPlayer owner = player(helper, 0);
        BlockPos pos = placeStand(helper, owner);
        CardDisplayStandBlockEntity stand = stand(helper, pos);
        check(helper, stand.ownerName().equals(owner.getGameProfile().getName()), "the placer owns the stand, owner is " + stand.ownerName());

        hold(owner, card(3));
        for (int i = 0; i < 3; i++) {
            use(owner, pos);
        }
        check(helper, stand.card().getCount() == 3, "3 clicks stock 3 cards, got " + stand.card().getCount());
        check(helper, owner.getMainHandItem().isEmpty(), "the cards leave the owner's hand, holding " + owner.getMainHandItem());
        check(helper, owner.containerMenu instanceof CardStandOwnerMenu, "the owner gets the owner menu, got " + owner.containerMenu);

        hold(owner, card(1, 7, false));
        use(owner, pos);
        check(helper, stand.card().getCount() == 3 && owner.getMainHandItem().getCount() == 1, "a different card does not go on the stand");
        hold(owner, ItemStack.EMPTY);

        use(owner, pos);
        owner.containerMenu.setCarried(new ItemStack(Items.DIAMOND, 64));
        owner.containerMenu.clicked(CardStandOwnerMenu.PRICE_SLOT, 0, ClickType.PICKUP, owner);
        check(helper, stand.priceItem().is(Items.DIAMOND) && stand.priceItem().getCount() == 1, "the price is 1 diamond, got " + stand.priceItem());
        check(helper, owner.containerMenu.getCarried().getCount() == 64, "setting the price keeps the carried diamonds, got " + owner.containerMenu.getCarried());
        owner.containerMenu.setCarried(ItemStack.EMPTY);

        int maxButton = CardStandOwnerMenu.BUTTON_AMOUNT + CardDisplayStandBlockEntity.MAX_PRICE;
        button(owner, maxButton);
        check(helper, stand.priceAmount() == CardDisplayStandBlockEntity.MAX_PRICE, "the max amount can be set, got " + stand.priceAmount());
        button(owner, maxButton + 1);
        check(helper, stand.priceAmount() == CardDisplayStandBlockEntity.MAX_PRICE, "an amount over the max is refused, got " + stand.priceAmount());
        button(owner, CardStandOwnerMenu.BUTTON_AMOUNT);
        check(helper, stand.priceAmount() == CardDisplayStandBlockEntity.MAX_PRICE, "an amount of 0 is refused, got " + stand.priceAmount());
        button(owner, CardStandOwnerMenu.BUTTON_AMOUNT + 3);
        check(helper, stand.priceAmount() == 3, "the amount can be set to 3, got " + stand.priceAmount());

        FriendlyByteBuf buf = new FriendlyByteBuf(Unpooled.buffer());
        ServerboundContainerButtonClickPacket.STREAM_CODEC.encode(buf, new ServerboundContainerButtonClickPacket(7, maxButton));
        int decoded = ServerboundContainerButtonClickPacket.STREAM_CODEC.decode(buf).buttonId();
        check(helper, decoded == maxButton, "button " + maxButton + " fits the button packet, got " + decoded);

        CompoundTag saved = stand.saveWithFullMetadata(helper.getLevel().registryAccess());
        BlockEntity loaded = BlockEntity.loadStatic(pos, helper.getLevel().getBlockState(pos), saved, helper.getLevel().registryAccess());
        check(helper, loaded instanceof CardDisplayStandBlockEntity reloaded && reloaded.card().getCount() == 3 && reloaded.priceItem().is(Items.DIAMOND)
                && reloaded.priceAmount() == 3 && reloaded.ownerName().equals(stand.ownerName()), "the stand keeps its stock, price and owner when saved, got " + saved);
        owner.closeContainer();
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void buyerPaysAndOwnerCollectsTheTill(GameTestHelper helper) {
        ServerPlayer owner = player(helper, 0);
        ServerPlayer buyer = player(helper, 2);
        BlockPos pos = placeStand(helper, owner);
        CardDisplayStandBlockEntity stand = stand(helper, pos);
        stock(owner, pos, 2, Items.DIAMOND, 3);

        hold(buyer, card(1));
        use(buyer, pos);
        check(helper, stand.card().getCount() == 2 && buyer.getMainHandItem().getCount() == 1, "a buyer cannot add cards to the stand");
        check(helper, buyer.containerMenu instanceof CardStandBuyerMenu, "a buyer gets the buyer menu, got " + buyer.containerMenu);
        buyer.closeContainer();
        buyer.getInventory().clearContent();

        buyer.setShiftKeyDown(true);
        use(buyer, pos);
        buyer.setShiftKeyDown(false);
        check(helper, stand.card().getCount() == 2 && cards(buyer) == 0, "a crouching buyer cannot take the cards");
        check(helper, buyer.containerMenu instanceof CardStandBuyerMenu, "a crouching buyer gets the buyer menu, got " + buyer.containerMenu);

        buyer.containerMenu.clicked(CardStandBuyerMenu.CARD_SLOT, 0, ClickType.PICKUP, buyer);
        buyer.containerMenu.clicked(CardStandBuyerMenu.CARD_SLOT, 0, ClickType.QUICK_MOVE, buyer);
        buyer.containerMenu.clicked(CardStandBuyerMenu.PRICE_SLOT, 0, ClickType.PICKUP, buyer);
        check(helper, stand.card().getCount() == 2 && buyer.containerMenu.getCarried().isEmpty() && cards(buyer) == 0, "a buyer cannot take from the menu slots");

        buyer.getInventory().setItem(0, new ItemStack(Items.DIAMOND, 2));
        button(buyer, CardStandBuyerMenu.BUTTON_BUY);
        check(helper, count(buyer, Items.DIAMOND) == 2 && stand.card().getCount() == 2 && stand.till().isEmpty(), "2 diamonds cannot pay 3");

        buyer.getInventory().setItem(OFFHAND_SLOT, new ItemStack(Items.DIAMOND, 5));
        button(buyer, CardStandBuyerMenu.BUTTON_BUY);
        check(helper, count(buyer, Items.DIAMOND) == 4, "buying takes 3 diamonds from the hotbar and offhand, got " + count(buyer, Items.DIAMOND));
        check(helper, cards(buyer) == 1 && stand.card().getCount() == 1, "the buyer gets 1 card, got " + cards(buyer) + ", stock " + stand.card().getCount());
        check(helper, stand.tillTotal() == 3, "the till has 3 diamonds, got " + stand.tillTotal());
        ItemStack bought = buyer.getInventory().items.stream().filter(stack -> stack.is(ModItems.TCG_CARD.get())).findFirst().orElse(ItemStack.EMPTY);
        check(helper, ItemStack.isSameItemSameComponents(bought, card(1)), "the bought card matches the one on the stand, got " + bought);

        buyer.moveTo(owner.getX() + 20, owner.getY(), owner.getZ());
        button(buyer, CardStandBuyerMenu.BUTTON_BUY);
        check(helper, count(buyer, Items.DIAMOND) == 4 && stand.card().getCount() == 1, "a buyer out of range cannot buy");
        buyer.moveTo(owner.getX() + 2, owner.getY(), owner.getZ());

        button(buyer, CardStandBuyerMenu.BUTTON_BUY);
        check(helper, count(buyer, Items.DIAMOND) == 1 && cards(buyer) == 2 && stand.card().isEmpty(), "the last card sells, stock is " + stand.card());
        button(buyer, CardStandBuyerMenu.BUTTON_BUY);
        check(helper, count(buyer, Items.DIAMOND) == 1 && cards(buyer) == 2, "a sold out stand takes no payment");
        check(helper, stand.buy(owner) == CardDisplayStandBlockEntity.Purchase.OWN_STAND, "the owner cannot buy from their own stand");
        buyer.closeContainer();

        use(owner, pos);
        check(helper, owner.containerMenu instanceof CardStandOwnerMenu menu && menu.tillTotal() == 6, "the owner menu shows 6 diamonds in the till");
        button(owner, CardStandOwnerMenu.BUTTON_COLLECT);
        check(helper, count(owner, Items.DIAMOND) == 6 && stand.till().isEmpty(), "the owner collects 6 diamonds, got " + count(owner, Items.DIAMOND));
        owner.closeContainer();
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void onlyTheOwnerCanBreakTheStand(GameTestHelper helper) {
        ServerPlayer owner = player(helper, 0);
        ServerPlayer other = player(helper, 2);
        BlockPos pos = placeStand(helper, owner);
        CardDisplayStandBlockEntity stand = stand(helper, pos);
        stock(owner, pos, 2, Items.EMERALD, 1);
        other.getInventory().setItem(0, new ItemStack(Items.EMERALD));
        use(other, pos);
        button(other, CardStandBuyerMenu.BUTTON_BUY);
        other.closeContainer();
        check(helper, stand.tillTotal() == 1, "the till has 1 emerald, got " + stand.tillTotal());

        check(helper, helper.getLevel().getBlockState(pos).getDestroyProgress(other, helper.getLevel(), pos) == 0.0F, "another player cannot mine the stand");
        check(helper, !other.gameMode.destroyBlock(pos) && isStand(helper, pos), "another survival player cannot break the stand");
        other.setGameMode(GameType.CREATIVE);
        check(helper, !other.gameMode.destroyBlock(pos) && isStand(helper, pos), "another creative player without op cannot break the stand");

        Vec3 ownerPos = owner.position();
        owner.moveTo(ownerPos.x, ownerPos.y + 40, ownerPos.z);
        other.moveTo(ownerPos.x, ownerPos.y + 40, ownerPos.z);
        helper.getLevel().explode(null, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 4.0F, Level.ExplosionInteraction.TNT);
        check(helper, isStand(helper, pos) && stand.card().getCount() == 1, "an explosion does not break the stand");
        clearDrops(helper, pos);
        owner.moveTo(ownerPos.x, ownerPos.y, ownerPos.z);

        check(helper, owner.gameMode.destroyBlock(pos) && !isStand(helper, pos), "the owner can break the stand");
        int stands = 0;
        int cards = 0;
        int emeralds = 0;
        for (ItemEntity drop : helper.getLevel().getEntitiesOfClass(ItemEntity.class, new AABB(pos).inflate(2))) {
            ItemStack stack = drop.getItem();
            if (stack.is(ModBlocks.CARD_DISPLAY_STAND_ITEM.get())) {
                stands += stack.getCount();
            } else if (stack.is(ModItems.TCG_CARD.get())) {
                cards += stack.getCount();
            } else if (stack.is(Items.EMERALD)) {
                emeralds += stack.getCount();
            }
        }
        check(helper, stands == 1 && cards == 1 && emeralds == 1, "the stand drops itself, its card and the till, got " + stands + " stand, " + cards + " card, " + emeralds + " emerald");
        helper.succeed();
    }

    @GameTest(template = EMPTY)
    public static void ownerTakesTheCardsBackWhileCrouching(GameTestHelper helper) {
        ServerPlayer owner = player(helper, 0);
        BlockPos pos = placeStand(helper, owner);
        CardDisplayStandBlockEntity stand = stand(helper, pos);
        stock(owner, pos, 4, Items.DIAMOND, 1);
        owner.getInventory().clearContent();

        owner.setShiftKeyDown(true);
        use(owner, pos);
        owner.setShiftKeyDown(false);
        check(helper, stand.card().isEmpty() && cards(owner) == 4, "crouching with an empty hand takes all 4 cards back, got " + cards(owner));
        check(helper, !stand.isForSale(), "an empty stand is not for sale");
        helper.succeed();
    }

    private static ServerPlayer player(GameTestHelper helper, int offset) {
        ServerPlayer player = PackRewardGameTests.mockPlayer(helper);
        BlockPos pos = helper.absolutePos(new BlockPos(1 + offset, 2, 3));
        player.moveTo(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, 180.0F, 30.0F);
        player.setGameMode(GameType.SURVIVAL);
        return player;
    }

    private static BlockPos placeStand(GameTestHelper helper, ServerPlayer owner) {
        helper.setBlock(new BlockPos(1, 1, 1), Blocks.STONE);
        BlockPos floor = helper.absolutePos(new BlockPos(1, 1, 1));
        hold(owner, new ItemStack(ModBlocks.CARD_DISPLAY_STAND_ITEM));
        owner.gameMode.useItemOn(owner, helper.getLevel(), owner.getMainHandItem(), InteractionHand.MAIN_HAND,
                new BlockHitResult(Vec3.atCenterOf(floor).add(0, 0.5, 0), Direction.UP, floor, false));
        BlockPos pos = floor.above();
        check(helper, isStand(helper, pos), "the stand item places a stand, got " + helper.getLevel().getBlockState(pos));
        return pos;
    }

    private static void stock(ServerPlayer owner, BlockPos pos, int cards, Item price, int amount) {
        hold(owner, card(cards));
        for (int i = 0; i < cards; i++) {
            use(owner, pos);
        }
        owner.containerMenu.setCarried(new ItemStack(price));
        owner.containerMenu.clicked(CardStandOwnerMenu.PRICE_SLOT, 0, ClickType.PICKUP, owner);
        owner.containerMenu.setCarried(ItemStack.EMPTY);
        button(owner, CardStandOwnerMenu.BUTTON_AMOUNT + amount);
        owner.closeContainer();
        hold(owner, ItemStack.EMPTY);
    }

    private static CardDisplayStandBlockEntity stand(GameTestHelper helper, BlockPos pos) {
        if (!(helper.getLevel().getBlockEntity(pos) instanceof CardDisplayStandBlockEntity stand)) {
            throw new IllegalStateException("no card display stand at " + pos);
        }
        return stand;
    }

    private static boolean isStand(GameTestHelper helper, BlockPos pos) {
        return helper.getLevel().getBlockState(pos).is(ModBlocks.CARD_DISPLAY_STAND.get());
    }

    private static void clearDrops(GameTestHelper helper, BlockPos pos) {
        helper.getLevel().getEntitiesOfClass(ItemEntity.class, new AABB(pos).inflate(6)).forEach(ItemEntity::discard);
    }

    private static ItemStack card(int count) {
        return card(count, 4, true);
    }

    private static ItemStack card(int count, int number, boolean holo) {
        ItemStack stack = new ItemStack(ModItems.TCG_CARD, count);
        stack.set(ModDataComponents.TCG_CARD.get(), new TcgCardData(Constants.id("base1"), number, holo));
        return stack;
    }

    private static void hold(ServerPlayer player, ItemStack stack) {
        player.setItemInHand(InteractionHand.MAIN_HAND, stack);
    }

    private static void use(ServerPlayer player, BlockPos pos) {
        player.gameMode.useItemOn(player, player.serverLevel(), player.getMainHandItem(), InteractionHand.MAIN_HAND,
                new BlockHitResult(Vec3.atCenterOf(pos), Direction.SOUTH, pos, false));
    }

    private static void button(ServerPlayer player, int id) {
        player.connection.handleContainerButtonClick(new ServerboundContainerButtonClickPacket(player.containerMenu.containerId, id));
    }

    private static int count(ServerPlayer player, Item item) {
        return player.getInventory().countItem(item);
    }

    private static int cards(ServerPlayer player) {
        return count(player, ModItems.TCG_CARD.get());
    }

    private static void check(GameTestHelper helper, boolean condition, String message) {
        if (!condition) {
            helper.fail(message);
        }
    }
}
